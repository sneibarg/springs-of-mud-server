import asyncio
import threading

import requests

from server.BackgroundIO import submit

from injector import inject

from game.GameData import GameData
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from server.TimeVal import gettimeofday, TimeVal, stall_until_last_time


class GameService:
    """Schedule pulses off-thread and dispatch live updates to their owner loop."""

    @inject
    def __init__(self, config: ServiceConfig):
        self.__name__ = "GameService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.game_data_endpoint = config.game_data_endpoint
        self.update_handler = None
        self._runtime_loop = None
        self._stop_requested = threading.Event()
        self._pending_update = None
        self._updates_suspended = False
        self._active_update_task = None
        self.game_data = self._fetch_game_data()
        self.enums = dict()
        self._load_enums()
        self.last_time: TimeVal = gettimeofday()

    def set_update_handler(self, update_handler):
        self.update_handler = update_handler

    def set_runtime_loop(self, loop) -> None:
        """Set the socket loop as owner of live sessions and world mutations."""
        self._runtime_loop = loop

    def stop(self) -> None:
        self._stop_requested.set()
        pending = self._pending_update
        if pending is not None:
            pending.cancel()

    async def start(self):
        await self._game_loop()

    async def pause_updates(self):
        self._updates_suspended = True
        active = self._active_update_task
        if active is not None and active is not asyncio.current_task():
            await asyncio.shield(active)

    def resume_updates(self):
        self._updates_suspended = False

    async def _handle_updates_if_active(self):
        if self._updates_suspended:
            return
        self._active_update_task = asyncio.current_task()
        try:
            await self.update_handler.handle_updates()
        finally:
            self._active_update_task = None

    async def _game_loop(self):
        while not self._stop_requested.is_set():
            try:
                await self._game_loop_iteration()
            except asyncio.CancelledError:
                if not self._stop_requested.is_set():
                    raise

    async def _run_updates(self):
        current_loop = asyncio.get_running_loop()
        owner = self._runtime_loop or current_loop
        if owner is current_loop:
            await self._handle_updates_if_active()
            return
        if owner.is_closed() or not owner.is_running():
            raise RuntimeError("The runtime owner loop is unavailable")
        # The scheduler waits for one complete pulse. Only the owner loop touches
        # live models; no thread lock is held while gameplay awaits messages/I/O.
        pending = asyncio.run_coroutine_threadsafe(self._handle_updates_if_active(), owner)
        self._pending_update = pending
        try:
            if self._stop_requested.is_set():
                pending.cancel()
            await asyncio.wrap_future(pending)
        finally:
            self._pending_update = None

    async def _game_loop_iteration(self):
        self.last_time = gettimeofday()
        current_time = self.last_time.tv_sec
        self.logger.debug(f"Current time: {current_time}; Pulses per second: {self.enums['gameParameters']['PULSE_PER_SECOND']}")
        await self._run_updates()
        if not self._stop_requested.is_set():
            stall_until_last_time(self.last_time, self.enums['gameParameters']['PULSE_PER_SECOND'])

    def _fetch_game_data(self):
        try:
            url = self.game_data_endpoint
            response = requests.get(url).json()[0]
            return GameData.from_json(response)
        except Exception as e:
            self.logger.error(f"Failed to load game data: {e}")
            raise RuntimeError(f"Failed to load game data: {e}")

    def queue_save_deny_list(self):
        return submit(self._persist_deny_list, str(self.game_data.id or ""),
                      {"denyList": list(self.game_data.denyList or [])})

    def queue_save_bans(self):
        # Only permanent bans cross the worker boundary; temporary rules stay live.
        payload = {'bans': self.game_data.site_bans.save_bans(),
                   'denyList': list(self.game_data.denyList or [])}
        return submit(self._persist_deny_list, str(self.game_data.id or ''), payload)

    def save_deny_list(self) -> bool:
        return self._persist_deny_list(str(self.game_data.id or ""),
                                       {"denyList": list(self.game_data.denyList or [])})

    def _persist_deny_list(self, game_data_id, payload) -> bool:
        if not game_data_id:
            self.logger.error("Refusing to save denyList without a game data id.")
            return False

        url = f"{self.game_data_endpoint}/{game_data_id}"
        try:
            response = requests.patch(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to save denyList to {url}: {e}")
            return False

    def _load_enums(self):
        from util.GenericUtil import GenericUtil
        for enum_name in self.game_data.enums:
            member_map = self.game_data.enums.get(enum_name)
            self.enums[enum_name] = GenericUtil.build_int_enum(enum_name, member_map)

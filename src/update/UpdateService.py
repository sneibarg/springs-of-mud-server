import asyncio

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List
from injector import inject
from area.AreaHandler import AreaHandler
from registry.AreaRegistry import AreaRegistry
from registry.MobileRegistry import MobileRegistry
from mobile.MobileHandler import MobileHandler

@dataclass
class ObjectUpdateTask:
    object_data: List[str]
    affect_data: List[str]


@dataclass
class AreaUpdateTask:
    area_id: str
    rooms: List[str]
    mobiles: List[str]
    shops: List[str]
    resets: List[str]
    specials: List[str]


class UpdateService:
    @inject
    def __init__(self, config, area_registry: AreaRegistry, mobile_registry: MobileRegistry, area_handler: AreaHandler, mobile_handler: MobileHandler, num_workers=4):
        self.config = config
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.area_registry = area_registry
        self.mobile_registry = mobile_registry
        self.area_handler = area_handler
        self.mobile_handler = mobile_handler
        self.stop_flag = False

    async def start(self):
        pass

    def update_handler(self):
        pass

    async def _update_areas(self):
        while not self.stop_flag:
            update_tasks = self._prepare_area_tasks()
            futures = []
            for task in update_tasks:
                future = asyncio.get_event_loop().run_in_executor(self.executor, self._update_area, task)
                futures.append(future)

            await asyncio.gather(*futures)

    def _update_area(self, task: AreaUpdateTask):
        for mobile_id in task.mobiles:
            self._update_mobile(mobile_id)
            self._check_respawn(task.area_id)

    def _update_mobile(self, mobile_id):
        pass

    def _check_respawn(self, area_id):
        pass

    def _prepare_area_tasks(self) -> List[AreaUpdateTask]:
        tasks = []
        area_list = self.area_handler.area_registry.registry.values()
        for area in area_list:
            passes = self.area_handler.passes_update_check(area.id, area.last_reset)
            if passes:
                tasks.append(AreaUpdateTask(area.id, area.rooms, area.mobiles, area.shops, area.resets, area.specials))
        return tasks

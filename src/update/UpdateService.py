import asyncio

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List
from area.AreaService import AreaService
from mobile.MobileService import MobileService


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
    def __init__(self, injector, config, num_workers=4):
        self.injector = injector
        self.config = config
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.mobile_service = self.injector.get(MobileService)
        self.area_service = self.injector.get(AreaService)
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
        area_list = self.area_service.get_areas()
        for area in area_list:
            passes = self.area_service.passes_update_check(area.id, area.last_reset)
            if passes:
                tasks.append(AreaUpdateTask(area.id, area.rooms, area.mobiles))
        return tasks

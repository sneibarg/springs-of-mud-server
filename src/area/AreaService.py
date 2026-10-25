from injector import inject
from area.Area import Area
from game.RegistryService import RegistryService
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class AreaService(FetchAndRegisterMixin):
    log_fetch_list_count = False

    @inject
    def __init__(self, config: ServiceConfig, registry_service: RegistryService):
        self.__name__ = "AreaService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.area_registry = self.registry_service.area_registry
        self.reset_registry = self.registry_service.reset_registry
        self.shop_registry = self.registry_service.shop_registry
        self.special_registry = self.registry_service.special_registry
        self.mobile_registry = self.registry_service.mobile_registry
        self.item_registry = self.registry_service.item_registry
        self.areas_endpoint = config.areas_endpoint
        self.load_areas()
        self.logger.info(f"Initialized AreaService instance with {len(self.area_registry.all_areas())} areas in memory.")

    def reload_areas(self) -> bool:
        return self._reload_collection(self.areas_endpoint, "areas", self.area_registry)

    def _validate_reload(self, registry, candidate) -> None:
        if self.registry_service.room_registry.all_rooms():
            raise ValueError("Area reload requires world migration; restart to replace a loaded world")
        for area in candidate.all_areas():
            self._lazy_load(area)

    def load_areas(self):
        self._fetch_and_register(self.areas_endpoint, "all areas")

    def load_area(self, area_name: str):
        url = f"{self.areas_endpoint}/name/{area_name}"
        return self._fetch_and_register(url, f"area '{area_name}'")

    def _build_fetch_item(self, area_data) -> Area:
        return Area.from_json(area_data)

    def _register_fetch_item(self, area: Area) -> None:
        self._lazy_load(area)
        self.area_registry.register(area)

    def _lazy_load(self, area: Area):
        area.rooms = [room for room in self.registry_service.room_registry.all_rooms() if room.area_id == area.id]
        for room in area.rooms:
            room.bind_area(area)
        area.resets = self.reset_registry.all_resets_by_area_id(area.id)
        area.shops = self.shop_registry.all_shops_by_area_id(area.id)
        area.specials = self.special_registry.all_specials_by_area_id(area.id)
        area.items = self.item_registry.all_items_by_area_id(area.id)
        area.mobiles = self.mobile_registry.all_mobiles_by_area_id(area.id)

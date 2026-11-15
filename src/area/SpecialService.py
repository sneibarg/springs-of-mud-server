from itertools import chain

from injector import inject
from area.RoomRegistry import RoomRegistry
from area.Special import Special
from area.SpecialRegistry import SpecialRegistry
from mobile.MobileRegistry import MobileRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class SpecialService(FetchAndRegisterMixin):
    log_fetch_list_count = False

    @inject
    def __init__(self, config: ServiceConfig, special_registry: SpecialRegistry,
                 mobile_registry: MobileRegistry, room_registry: RoomRegistry):
        self.__name__ = "SpecialService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.specials_endpoint = config.specials_endpoint
        self.special_registry = special_registry
        self.mobile_registry = mobile_registry
        self.room_registry = room_registry
        self.load_specials()

    def reload_specials(self) -> bool:
        """Reload definitions and live bindings on the world event loop."""
        return self._reload_collection(self.specials_endpoint, "specials", self.special_registry)

    def _publish_registry(self, registry: SpecialRegistry, candidate: SpecialRegistry) -> None:
        prototypes = self.mobile_registry.all_mobiles()
        prototype_areas = {str(mobile.vnum): mobile.area_id for mobile in prototypes}
        specials = candidate.all_specials()
        assignments = {(special.area_id, special.mob_vnum): special for special in specials if special.mob_vnum}
        by_id = {special.id: special for special in specials}
        live_mobiles = (mobile for room in self.room_registry.all_rooms() for mobile in room.mobiles_in_room())
        bindings = []
        for mobile in chain(prototypes, live_mobiles):
            if mobile.special_override_id is not None:
                bindings.append((mobile, mobile.special_assignment_area_id, by_id.get(mobile.special_override_id)))
                continue
            area_id = mobile.special_assignment_area_id
            if area_id is None:
                area_id = prototype_areas.get(str(mobile.vnum))
            if area_id is not None:
                bindings.append((mobile, area_id, assignments.get((str(area_id), str(mobile.vnum)))))

        super()._publish_registry(registry, candidate)
        for mobile, area_id, special in bindings:
            mobile.special_assignment_area_id = area_id
            mobile.bind_special(special)

    def load_specials(self):
        self._load_collection(self.specials_endpoint, "specials")
        self.logger.info(f"Loaded {len(self.special_registry.all_specials())} specials.")

    def load_special(self, special_name: str):
        url = f"{self.specials_endpoint}/name/{special_name}"
        return self._fetch_and_register(url, f"special '{special_name}'")

    def _build_fetch_item(self, special_data) -> Special:
        return Special.from_json(special_data)

    def _register_fetch_item(self, special: Special) -> None:
        self.special_registry.register(special)

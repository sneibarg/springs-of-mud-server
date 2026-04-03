from registries import Registry
from interp.Social import Social
from server.LoggerFactory import LoggerFactory


class SocialRegistry(Registry[Social]):
    lookup_attrs = ('id', 'name')

    def __init__(self):
        super().__init__()

        self.__name__ = "SocialRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_socials(self) -> list[Social]:
        return list(self.registry.values())
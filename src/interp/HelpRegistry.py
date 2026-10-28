from registries import Registry
from interp.HelpEntry import HelpEntry
from server.LoggerFactory import LoggerFactory


class HelpRegistry(Registry[HelpEntry]):
    lookup_attrs = ('id', 'keyword')

    def __init__(self):
        super().__init__()

        self.__name__ = "HelpRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_helps(self) -> set[HelpEntry]:
        return self._items

    def find_topic(self, topic: str) -> HelpEntry | None:
        query = HelpEntry.normalize_topic(topic)
        if not query:
            return None
        matches = [entry for entry in self.all_helps() if query in entry.lookup_topics()]
        # Legacy or remote duplicate aliases still produce exactly one stable result.
        return min(matches, key=lambda entry: (HelpEntry.normalize_topic(entry.keyword) != query, entry.id), default=None)

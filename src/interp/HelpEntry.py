from dataclasses import dataclass
import re


@dataclass
class HelpEntry:
    id: str
    keyword: str
    text: str
    level: int
    topics: list[str] | None = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, HelpEntry):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        if isinstance(data, cls):
            return data
        raw_id = data.get('id') or data.get('_id')
        if isinstance(raw_id, dict):
            raw_id = raw_id.get('$oid')
        topics = data.get('topics')
        if isinstance(topics, str):
            topics = [topics]
        return cls(id=str(raw_id or GenericUtil.generate_mongo_id()),
                   keyword=str(data.get('keyword', '') or '').lower(),
                   text=str(data.get('text', '') or ''), level=int(data.get('level', 0)),
                   topics=None if topics is None else list(topics))

    @staticmethod
    def normalize_topic(value: str) -> str:
        value = str(value or '').strip()
        if len(value) > 1 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        return ' '.join(value.split()).casefold()

    def lookup_topics(self) -> set[str]:
        if self.topics is not None:
            return {self.normalize_topic(topic) for topic in self.topics if self.normalize_topic(topic)}
        # Legacy titles are aliases, never prose or an imported tilde record.
        if '\n' in self.keyword or '\r' in self.keyword or '~' in self.keyword:
            return set()
        aliases = re.findall(r"'([^']+)'|\"([^\"]+)\"|(\S+)", self.keyword)
        return {self.normalize_topic(next(part for part in match if part)) for match in aliases}

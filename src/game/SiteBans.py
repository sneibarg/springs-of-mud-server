from dataclasses import dataclass


@dataclass(frozen=True)
class SiteBan:
    name: str
    level: int
    kind: str = 'all'
    permanent: bool = False
    prefix: bool = False
    suffix: bool = False

    @property
    def pattern(self):
        return ('*' if self.prefix else '') + self.name + ('*' if self.suffix else '')

    def matches(self, host):
        host = str(host or '').strip().lower()
        if self.prefix and self.suffix:
            return self.name in host
        if self.prefix:
            return host.endswith(self.name)
        if self.suffix:
            return host.startswith(self.name)
        return host == self.name


class SiteBans:
    """ROM site-ban policy; transport and persistence are owned by callers."""

    def __init__(self):
        self.entries = []

    def load_bans(self, records):
        entries = []
        for record in records or []:
            ban = SiteBan(name=str(record['name']).strip().lower(), level=int(record['level']),
                          kind=str(record.get('type', 'all')).lower(), permanent=True,
                          prefix=bool(record.get('prefix', False)), suffix=bool(record.get('suffix', False)))
            if not ban.name or ban.kind not in ('all', 'newbies', 'permit'):
                raise ValueError('Invalid site ban')
            entries.append(ban)
        self.entries = entries

    def save_bans(self):
        return [dict(name=ban.name, level=ban.level, type=ban.kind, prefix=ban.prefix, suffix=ban.suffix)
                for ban in self.entries if ban.permanent]

    def check_ban(self, host, kind='all'):
        return any(ban.kind == kind and ban.matches(host) for ban in self.entries)

    def ban_site(self, pattern, option, trust, permanent=False):
        kind = next((kind for kind in ('all', 'newbies', 'permit') if kind.startswith(option or 'all')), None)
        if kind is None:
            return 'invalid_option', None
        pattern = str(pattern or '').strip().lower()
        name = pattern.removeprefix('*').removesuffix('*')
        if not name or '*' in name:
            return 'no_argument', None
        existing = next((ban for ban in self.entries if ban.name == name), None)
        if existing is not None and existing.level > trust:
            return 'insufficient_level', None
        self.entries = [ban for ban in self.entries if ban.name != name]
        ban = SiteBan(name, trust, kind, permanent, pattern.startswith('*'), pattern.endswith('*'))
        self.entries.insert(0, ban)
        return 'default', ban

    def allow(self, name, trust):
        name = str(name or '').strip().lower()
        for ban in self.entries:
            if ban.name == name:
                if ban.level > trust:
                    return 'insufficient_level'
                self.entries.remove(ban)
                return 'removed'
        return 'no_such_ban'

from typing import Any

import requests


class FetchAndRegisterMixin:
    fetch_error_return = None
    log_fetch_list_count = True

    def _fetch_and_register(self, url: str, description: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for raw_item in data:
                    item = self._build_fetch_item(raw_item)
                    if item is None:
                        continue
                    self._register_fetch_item(item)
                    count += 1
                self._log_fetch_list(description, count)
                return None

            item = self._build_fetch_item(data)
            if item is None:
                return self.fetch_error_return
            self._register_fetch_item(item)
            self.logger.info(f"Loaded {description}.")
            return item

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return self.fetch_error_return
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return self.fetch_error_return

    def _reload_collection(self, url: str, description: str, registry) -> bool:
        """Build and validate a complete replacement before publishing any entries.

        The registries package has no snapshot replacement API. Keep its storage
        adaptation here, preserving the injected registry object and its lock.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("A collection reload requires a JSON list")
            candidate = type(registry)()
            for raw_item in data:
                item = self._build_reload_item(raw_item)
                if item is None or ('id' in candidate.lookup_attrs
                                    and not str(getattr(item, 'id', '') or '').strip()):
                    raise ValueError("Collection contains an invalid document or missing id")
                candidate.register(item)
            for item in self._reload_extra_items():
                candidate.register(item)
            candidate.populate()
            self._validate_reload(registry, candidate)
            self._publish_registry(registry, candidate)
            self.logger.info(f"Reloaded {len(candidate)} {description}.")
            return True
        except Exception as error:
            self.logger.error(f"Failed to reload {description}; previous registry retained: {error}", exc_info=True)
            return False

    def _reload_extra_items(self):
        return ()

    def _build_reload_item(self, raw_item):
        return self._build_fetch_item(raw_item)

    @staticmethod
    def _publish_registry(registry, candidate) -> None:
        with registry._lock:
            registry.__dict__.update(_items=candidate._items,
                                     _registry=candidate._registry, state=candidate.state)

    def _validate_reload(self, registry, candidate) -> None:
        """Services owning live world objects may reject definition replacement."""

    def _build_fetch_item(self, raw_item: Any):
        raise NotImplementedError

    def _register_fetch_item(self, item: Any) -> None:
        raise NotImplementedError

    def _log_fetch_list(self, description: str, count: int) -> None:
        if self.log_fetch_list_count:
            self.logger.info(f"Loaded {count} {description}.")

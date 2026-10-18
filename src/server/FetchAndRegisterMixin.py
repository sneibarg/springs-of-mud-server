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

    def _build_fetch_item(self, raw_item: Any):
        raise NotImplementedError

    def _register_fetch_item(self, item: Any) -> None:
        raise NotImplementedError

    def _log_fetch_list(self, description: str, count: int) -> None:
        if self.log_fetch_list_count:
            self.logger.info(f"Loaded {count} {description}.")

import re

from typing import Dict, Any


class ServerUtil:
    pass

    @staticmethod
    def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        def camel_case_to_snake_case(string: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        snake_case_dict = {}
        for key, value in dictionary.items():
            snake_case_dict[camel_case_to_snake_case(key)] = value
        return snake_case_dict

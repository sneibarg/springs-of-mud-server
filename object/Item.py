from dataclasses import dataclass


@dataclass
class Item:
    id: str
    area_id: str
    vnum: str
    description: str
    name: str
    short_description: str
    long_description: str
    item_type: str
    weight: str
    extra_flags: str
    wear_flags: str
    value: str
    level: str
    affect_data: list
    extra_descr: list

    def __post_init__(self):
        self.__name__ = "Item"
        from server import LoggerFactory
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        import json
        from utilities.server_util import camel_to_snake_case
        data = camel_to_snake_case(json.loads(data))
        return cls(**data)

    def get_name(self):
        return self.name

    def print_name(self, writer):
        msg = "\t" + self.name + "\r\n"
        writer.write(msg.encode('utf-8'))

    def print_description(self, writer):
        if writer is None:
            self.logger.debug("print_description: writer="+str(writer)+", item_id="+str(id))
            return
        msg = "\r\n\n" + self.long_description + "\r\n\n"
        writer.write(msg.encode('utf-8'))


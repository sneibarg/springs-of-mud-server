import subprocess
import sys
import textwrap
import unittest


class TestAreaPetShopResets(unittest.TestCase):
    def test_pet_shop_mobile_resets_set_act_pet(self):
        code = r'''
import os
import sys
import types
from enum import IntEnum
from types import SimpleNamespace
from unittest.mock import Mock, patch

root = os.getcwd()
src = os.path.join(root, "src")
sys.path.insert(0, src)

for package_name in ("api", "area", "fight", "game", "interp", "mobile", "item", "player", "skill", "util"):
    package = types.ModuleType(package_name)
    package.__path__ = [os.path.join(src, package_name)]
    sys.modules[package_name] = package

registries = types.ModuleType("registries")
class Registry:
    def __class_getitem__(cls, _item):
        return cls
registries.Registry = Registry
sys.modules["registries"] = registries

injector = types.ModuleType("injector")
injector.inject = lambda target: target
sys.modules["injector"] = injector

server = types.ModuleType("server")
server.__path__ = [os.path.join(src, "server")]
sys.modules["server"] = server

logger_factory = types.ModuleType("server.LoggerFactory")
class LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return Mock()
logger_factory.LoggerFactory = LoggerFactory
sys.modules["server.LoggerFactory"] = logger_factory

messaging = types.ModuleType("server.messaging")
messaging.MessageBus = object
sys.modules["server.messaging"] = messaging

character_api = types.ModuleType("api.CharacterApi")
class CharacterApi:
    @staticmethod
    def enum_provider():
        return object()

    @staticmethod
    def enum_bit(enum_obj, *names):
        for name in names:
            if enum_obj is not None and name in enum_obj.__members__:
                return int(enum_obj[name].value)
        return 0

    @staticmethod
    def set_bit(flag, bit):
        return int(flag) | int(bit)
character_api.CharacterApi = CharacterApi
sys.modules["api.CharacterApi"] = character_api

item_api = types.ModuleType("api.ItemApi")
class ItemApi:
    @staticmethod
    def is_set(flag, bit):
        return (int(flag) & int(bit)) != 0
item_api.ItemApi = ItemApi
sys.modules["api.ItemApi"] = item_api

game_api = types.ModuleType("api.GameApi")
class GameApi:
    pass
game_api.GameApi = GameApi
sys.modules["api.GameApi"] = game_api

for module_name, class_name in (
    ("area.Area", "Area"),
    ("area.AreaRegistry", "AreaRegistry"),
    ("area.RoomRegistry", "RoomRegistry"),
    ("area.ShopRegistry", "ShopRegistry"),
    ("mobile.Mobile", "Mobile"),
    ("mobile.MobileRegistry", "MobileRegistry"),
    ("item.Item", "Item"),
    ("item.ItemRegistry", "ItemRegistry"),
    ("player.CharacterRegistry", "CharacterRegistry"),
):
    module = types.ModuleType(module_name)
    setattr(module, class_name, object)
    sys.modules[module_name] = module

mobile_util = types.ModuleType("util.MobileUtil")
class MobileUtil:
    @staticmethod
    def create_mobile(*_args, **_kwargs):
        return None
mobile_util.MobileUtil = MobileUtil
sys.modules["util.MobileUtil"] = mobile_util

item_util = types.ModuleType("util.ItemUtil")
class ItemUtil:
    pass
item_util.ItemUtil = ItemUtil
sys.modules["util.ItemUtil"] = item_util

for module_name, class_name in (
    ("fight.FightHandler", "FightHandler"),
    ("game.EnumProvider", "EnumProvider"),
    ("game.Equipped", "Equipped"),
    ("game.WeatherHandler", "WeatherHandler"),
    ("game.RegistryService", "RegistryService"),
    ("interp.Context", "Context"),
    ("api.InterpApi", "InterpApi"),
    ("api.SpellApi", "SpellApi"),
    ("item.EffectHandler", "EffectHandler"),
    ("player.Character", "Character"),
    ("skill.Ability", "Ability"),
    ("skill.SpellContext", "SpellContext"),
):
    module = types.ModuleType(module_name)
    setattr(module, class_name, object)
    sys.modules[module_name] = module

for module_name, class_name in (
    ("util.InfoUtil", "InfoUtil"),
    ("util.FightUtil", "FightUtil"),
    ("util.CommunicationsUtil", "CommunicationsUtil"),
    ("util.PlayerUtil", "PlayerUtil"),
):
    module = types.ModuleType(module_name)
    setattr(module, class_name, object)
    sys.modules[module_name] = module

from area.AreaHandler import AreaHandler
from area.Reset import Reset

class RoomFlags(IntEnum):
    ROOM_PET_SHOP = 8

class ActBits(IntEnum):
    ACT_PET = 16

class AffectedBits(IntEnum):
    AFF_CHARM = 32

class CommFlags(IntEnum):
    COMM_NOTELL = 64
    COMM_NOSHOUT = 128
    COMM_NOCHANNELS = 256

class TestStatusFlags:
    def __init__(self, act=0):
        self.act = act
        self.affected_by = 0
        self.comm = 0

    def set_flag(self, name, bit):
        if name not in ("act", "affected_by", "comm"):
            raise AssertionError(name)
        setattr(self, name, getattr(self, name) | int(bit))

def room(vnum, flags=0):
    result = SimpleNamespace(id=f"room-{vnum}", area_id="area1", vnum=str(vnum), room_flags=flags, mobiles={})
    result.add_mobile_to_room = lambda mob: result.mobiles.__setitem__(mob.id, mob)
    result.player_targets = lambda _character: []
    return result

def build_handler(rooms):
    def get_room(*_args, **kwargs):
        return rooms.get(str(kwargs.get("vnum", "")))
    room_registry = Mock()
    room_registry.get.side_effect = get_room
    room_registry.get_or_none.side_effect = get_room
    room_registry.all_rooms.return_value = list(rooms.values())
    enum_provider = SimpleNamespace(get=lambda name: {
        "wellKnownRoomVnums": SimpleNamespace(ROOM_VNUM_SCHOOL=3001),
        "exitFlags": SimpleNamespace(),
        "itemFlags": SimpleNamespace(ITEM_INVENTORY=SimpleNamespace(value=32)),
        "roomFlags": RoomFlags,
        "actBits": ActBits,
    }[name])
    return AreaHandler(
        message_bus=Mock(),
        area_registry=Mock(),
        room_registry=room_registry,
        item_registry=Mock(),
        mobile_registry=Mock(),
        shop_registry=Mock(find_by_keeper_vnum=Mock(return_value=None)),
        enum_provider=enum_provider,
        character_registry=Mock(),
    )

def reset(mob_vnum, room_vnum):
    return Reset(id="r1", area_id="area1", command="M", arg1=str(mob_vnum), arg2="1", arg3=str(room_vnum), arg4="1", comment="")

shop = room(3031, RoomFlags.ROOM_PET_SHOP.value)
stock = room(3032)
handler = build_handler({"3031": shop, "3032": stock})
handler.mobile_registry.get.return_value = SimpleNamespace(vnum="3090", room_id="", specials=[])
live_mob = SimpleNamespace(id="mob1", vnum="3090", status_flags=TestStatusFlags())
with patch("area.AreaHandler.MobileUtil.create_mobile", return_value=live_mob):
    last, mob = handler._do_mob_reset(True, reset(3090, 3032))
assert last is True
assert mob is live_mob
assert live_mob.status_flags.act == ActBits.ACT_PET.value
assert "mob1" in stock.mobiles

nabil = room(9621, RoomFlags.ROOM_PET_SHOP.value)
hall = room(9705)
back_room = room(9706)
handler = build_handler({"9621": nabil, "9705": hall, "9706": back_room})
handler.mobile_registry.get.return_value = SimpleNamespace(vnum="3097", room_id="", specials=[])
live_mob = SimpleNamespace(id="mob2", vnum="3097", status_flags=TestStatusFlags())
with patch("area.AreaHandler.MobileUtil.create_mobile", return_value=live_mob):
    handler._do_mob_reset(True, reset(3097, 9706))
assert live_mob.status_flags.act == ActBits.ACT_PET.value

plain_previous = room(4000)
plain_room = room(4001)
handler = build_handler({"4000": plain_previous, "4001": plain_room})
handler.mobile_registry.get.return_value = SimpleNamespace(vnum="400", room_id="", specials=[])
live_mob = SimpleNamespace(id="mob3", vnum="400", status_flags=TestStatusFlags())
with patch("area.AreaHandler.MobileUtil.create_mobile", return_value=live_mob):
    handler._do_mob_reset(True, reset(400, 4001))
assert live_mob.status_flags.act == 0

from area.Shop import Shop

buyer = SimpleNamespace(id="buyer1", name="Buyer", gold=5, silver=0, pet=None)
shop_room = room(3031)
shop_room.area_id = "midgaard"
pet = SimpleNamespace(
    id="pet1",
    name="kitten",
    description="A kitten.\r\n",
    room_id="room-3032",
    area_id="midgaard",
    status_flags=TestStatusFlags(),
)
with patch("area.Shop.MobileUtil.create_mobile", return_value=pet):
    purchased = Shop.complete_pet_purchase(
        buyer,
        shop_room,
        SimpleNamespace(),
        "fluffy",
        25,
        ActBits,
        AffectedBits,
        CommFlags,
    )
assert purchased is pet
assert pet.master is buyer
assert pet.leader is buyer
assert buyer.pet is pet
assert pet.room_id == "room-3031"
assert pet.area_id == "midgaard"
assert pet.status_flags.act == ActBits.ACT_PET.value
assert pet.status_flags.affected_by == AffectedBits.AFF_CHARM.value
assert pet.status_flags.comm == (CommFlags.COMM_NOTELL.value | CommFlags.COMM_NOSHOUT.value | CommFlags.COMM_NOCHANNELS.value)
assert pet.name == "kitten fluffy"
assert buyer.gold == 4 and buyer.silver == 75

from interp.commands.Object import Object

commands = Object.__new__(Object)
registered = []
commands.registry_service = SimpleNamespace(character_registry=SimpleNamespace(register=lambda entity: registered.append(entity)))
commands.act_bits = ActBits
commands.affected_bits = AffectedBits
commands.comm_flags = CommFlags
commands._render_command_message = lambda _context, key, **_tokens: key
command_context = SimpleNamespace(buy_pet_proto=SimpleNamespace(), buy_pet_name="", buy_cost=0)
with patch("interp.commands.Object.Shop.complete_pet_purchase", return_value=pet):
    payload = commands._finish_buy_pet(buyer, shop_room, command_context)
assert registered == [pet]
assert payload["to_char"] == "pet_purchased"
'''
        result = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(code)],
            cwd=".",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()

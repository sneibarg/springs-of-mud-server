"""Save and restore the persistent state of a purchased mobile."""

from game.Equipped import Equipped
from game.StatusFlags import StatusFlags
from item.Effect import Effect
from item.Item import Item
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from mobile.Mobile import Mobile
from player.CharacterAttributes import CharacterAttributes
from server.WireCodec import serialize_wire_value
from util.GenericUtil import GenericUtil


_PET_EXCLUDED_FIELDS = frozenset({
    'lock', 'room_id', 'area_id', 'origin_area_id', 'fighting', 'master', 'leader',
    'count', 'killed', 'extra_flags', 'inventory', 'equipped', '_bitfield_write_enabled', '_initialized',
})
_ITEM_EXCLUDED_FIELDS = frozenset({'room_data'})


def snapshot_pet(pet: Mobile, fighting_position: int, standing_position: int) -> dict:
    snapshot = serialize_wire_value(pet, excluded_fields=_PET_EXCLUDED_FIELDS)
    snapshot['inventory'] = serialize_wire_value(pet.inventory, excluded_fields=_ITEM_EXCLUDED_FIELDS)
    snapshot['equipped'] = serialize_wire_value(pet.equipped, excluded_fields=_ITEM_EXCLUDED_FIELDS)
    snapshot.update(hit=pet.hit, maxHit=pet.max_hit, mana=pet.mana, maxMana=pet.max_mana)
    snapshot['damageBonusInDamRoll'] = True
    snapshot['statusFlags'].update(pulseWait=0, pulseDaze=0)
    if pet.fighting is not None or snapshot['characterAttributes']['position'] == fighting_position:
        snapshot['characterAttributes']['position'] = standing_position
    return snapshot


def restore_pet(snapshot: dict, owner, *, item_registry=None) -> Mobile:
    data = GenericUtil.camel_to_snake_case(snapshot)
    data.pop('creation_order', None)
    damage_bonus_in_dam_roll = data.pop('damage_bonus_in_dam_roll', False)
    resources = [data.pop(name) for name in ('hit', 'max_hit', 'mana', 'max_mana')]
    data['area_id'] = owner.area_id
    data['status_flags'] = StatusFlags.from_json(data['status_flags'])
    data['character_attributes'] = CharacterAttributes.from_json(data['character_attributes'])
    armor = data['armor_class']
    data['armor_class'] = ArmorClass(**armor) if armor is not None else None
    for name in ('hit_dice', 'mana_dice', 'damage_dice'):
        dice = data[name]
        data[name] = Dice(**dice) if dice is not None else None
    data['effects'] = [Effect.from_json(effect) for effect in data['effects']]
    data['inventory'] = [_restore_item(item, owner.area_id, item_registry) for item in data['inventory']]
    equipment = GenericUtil.camel_to_snake_case(data['equipped'])
    inventory = {item.id: item for item in data['inventory']}
    data['equipped'] = Equipped(**{
        slot: inventory.get(item['id']) or _restore_item(item, owner.area_id, item_registry)
        for slot, item in equipment.items() if item is not None
    })
    pet = Mobile.from_json(data)
    if not damage_bonus_in_dam_roll and pet.damage_dice is not None:
        # Older snapshots stored the modifiers here and applied the dice bonus during the attack.
        pet.dam_roll += pet.damage_dice.bonus
    pet.hit, pet.max_hit, pet.mana, pet.max_mana = resources
    pet.master = pet.leader = owner
    for item in vars(pet.equipped).values():
        if item is not None:
            item._effect_wearer = pet
    return pet


def _restore_item(snapshot: dict, area_id: str, item_registry) -> Item:
    data = GenericUtil.camel_to_snake_case(snapshot)
    if 'area_id' not in data or 'extra_flags' not in data:
        # Earlier pet snapshots omitted these fields from every item in the tree.
        prototype = item_registry.get_or_none(vnum=str(data['vnum'])) if item_registry is not None else None
        data.setdefault('area_id', prototype.area_id if prototype is not None else area_id)
        data.setdefault('extra_flags', prototype.extra_flags if prototype is not None else '0')
    data['contains'] = [_restore_item(child, area_id, item_registry) for child in data.get('contains') or []]
    return Item.from_json(data)

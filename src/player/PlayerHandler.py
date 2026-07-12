import inspect

from dataclasses import fields
from typing import Any
from injector import inject

from api.InterpApi import InterpApi
from combat.CombatHandler import FightHandler
from game.WizHandler import WizHandler
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.Info import Info
from interp.commands.Movement import Movement
from interp.commands.Communications import Communications
from interp.commands.Fight import Fight
from interp.commands.Object import Object
from interp.commands.Wiz import Wiz
from player.Character import Character
from api.CharacterApi import CharacterApi
from util.GenericUtil import GenericUtil
from util.InfoUtil import InfoUtil
from util.InterpUtil import InterpUtil
from util.CommunicationsUtil import CommunicationsUtil
from util.ItemUtil import ItemUtil
from util.PlayerUtil import PlayerUtil
from skill.Ability import Ability
from server.messaging import MessageBus
from server.LoggerFactory import LoggerFactory


class PlayerHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 interp_api: InterpApi,
                 registry_service: RegistryService,
                 fight_handler: FightHandler,
                 wiz_handler: WizHandler,
                 communications_commands: Communications,
                 fight_commands: Fight,
                 info_commands: Info,
                 movement_commands: Movement,
                 object_commands: Object,
                 wiz_commands: Wiz):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.interp_api = interp_api
        self.registry_service = registry_service
        self.player_registry = registry_service.player_registry
        self.character_registry = registry_service.character_registry
        self.area_registry = registry_service.area_registry
        self.room_registry = registry_service.room_registry
        self.interp_registry = registry_service.interp_registry
        self.social_registry = registry_service.social_registry
        self.fight_handler = fight_handler
        self.wiz_handler = wiz_handler
        self.communications_commands = communications_commands
        self.fight_commands = fight_commands
        self.info_commands = info_commands
        self.movement_commands = movement_commands
        self.object_commands = object_commands
        self.wiz_commands = wiz_commands
        self.logger = LoggerFactory.get_logger(__name__)

    async def do_quit(self, character: Character, context: Context):
        payload = self.info_commands.do_quit(context)
        message = self.message_bus.text_to_message(payload["to_char"])
        await self.message_bus.send_to_character(character.id, message)
        if payload.get("blocked"):
            return
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        if room is not None:
            for viewer in room.characters.values():
                if viewer.id == character.id:
                    continue
                if CharacterApi.can_see(viewer, character, room):
                    text = payload["to_room"]
                else:
                    text = "Someone has left the game.\r\n"
                await self.message_bus.send_to_character(viewer.id, self.message_bus.text_to_message(text))
            room.remove_player_from_room(character)
        await context.disconnect()

    async def do_who(self, character):
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(self.info_commands.do_who(character))
        )

    async def do_help(self, character: Character, context: Context):
        argument = context.result if isinstance(context.result, str) else " ".join(context.parameters or [])
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(self.info_commands.do_help(argument))
        )
        context.finish()

    async def do_look(self, character: Character, context: Context):
        self._classify_look(character, context)
        payload = await self.info_commands.do_look(character, context)
        if payload is not None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["to_char"]))

    def _classify_look(self, character: Character, context: Context) -> None:
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        context.look_mode = "room"
        context.look_in_argument = ""
        context.look_in_target = None
        context.look_target_character = None
        context.look_direction_exit = None
        if room is None:
            return

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 in ("", "auto"):
            return

        if arg1 in ("i", "in", "on"):
            context.look_mode = "in"
            context.look_in_argument = (context.parameters[1] if context.parameters and len(context.parameters) > 1 else "").strip().lower()
            context.look_in_target = character.find_inventory_item(context.look_in_argument) or room.find_room_item(context.look_in_argument)
            return

        target = PlayerUtil.get_target(character, arg1, room)
        if target is not None:
            context.look_mode = "target"
            context.look_target_character = target
            return

        if self._look_item_or_extra_exists(character, room, arg1):
            context.look_mode = "item_or_extra"
            return

        direction = room.direction_index(arg1) if hasattr(room, "direction_index") else -1
        if direction >= 0:
            context.look_mode = "direction"
            context.look_direction_exit = room.get_exit(direction) if hasattr(room, "get_exit") else None
            return

        context.look_mode = "unknown"

    @staticmethod
    def _look_item_or_extra_exists(character: Character, room, argument: str) -> bool:
        _number, token = InterpUtil.number_argument(argument)
        wanted = (token or "").strip().lower()
        if not wanted:
            return False

        for item in list(character.get_items()) + list(room.contents.values()):
            if not ItemUtil.can_see_object(room, character, item):
                continue

            extra = getattr(item, "extra_description", None)
            extra_keyword = getattr(extra, "keyword", None) if extra is not None else None
            if isinstance(extra, dict):
                extra_keyword = extra.get("keyword")
            if extra and InfoUtil.look_keyword_matches(wanted, extra_keyword or ""):
                return True

            if InfoUtil.look_keyword_matches(wanted, getattr(item, "name", "") or ""):
                return True

        room_extra = getattr(room, "extra_description", None)
        if isinstance(room_extra, dict):
            room_extra_keyword = room_extra.get("keyword")
        else:
            room_extra_keyword = getattr(room_extra, "keyword", "")
        return bool(room_extra and InfoUtil.look_keyword_matches(wanted, room_extra_keyword or ""))

    async def do_scroll(self, character: Character, context: Context):
        text = self.info_commands.do_scroll(character, context)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_wimpy(self, character: Character, context: Context):
        text = self.info_commands.do_wimpy(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_score(self, character: Character, context: Context):
        text = self.info_commands.do_score(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_time(self, character: Character, context: Context):
        text = self.info_commands.do_time(context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_weather(self, character: Character, context: Context):
        text = self.info_commands.do_weather(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_where(self, character: Character, context: Context):
        text = self.info_commands.do_where(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_consider(self, character: Character, context: Context):
        text = self.info_commands.do_consider(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_title(self, character: Character, context: Context):
        text = self.info_commands.do_title(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_description(self, character: Character, context: Context):
        text = self.info_commands.do_description(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_report(self, character: Character, context: Context):
        payload = self.info_commands.do_report(character)
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(payload["to_char"])
        )
        if len(payload["people"]) > 0:
            await self.message_bus.send_to_room(
                self.message_bus.text_to_message(payload["to_room"]),
                payload["people"]
            )

    async def do_autolist(self, character: Character, context: Context):
        text = self.info_commands.do_autolist(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autoassist(self, character: Character, context: Context):
        text = self.info_commands.do_autoassist(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autoexit(self, character: Character, context: Context):
        text = self.info_commands.do_autoexit(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autogold(self, character: Character, context: Context):
        text = self.info_commands.do_autogold(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autoloot(self, character: Character, context: Context):
        text = self.info_commands.do_autoloot(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autosac(self, character: Character, context: Context):
        text = self.info_commands.do_autosac(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autosplit(self, character: Character, context: Context):
        text = self.info_commands.do_autosplit(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_worth(self, character: Character, context: Context):
        text = self.info_commands.do_worth(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_affects(self, character: Character, context: Context):
        text = self.info_commands.do_affects(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_brief(self, character: Character, context: Context):
        text = self.info_commands.do_brief(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_compact(self, character: Character, context: Context):
        text = self.info_commands.do_compact(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_combine(self, character: Character, context: Context):
        text = self.info_commands.do_combine(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_noloot(self, character: Character, context: Context):
        text = self.info_commands.do_noloot(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_nofollow(self, character: Character, context: Context):
        text = self.info_commands.do_nofollow(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_nosummon(self, character: Character, context: Context):
        text = self.info_commands.do_nosummon(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_read(self, character: Character, context: Context):
        payload = self.info_commands.do_read(context)
        if payload.get("look"):
            text = await self.info_commands.do_look(character, context)
            if text:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            if not context.done:
                await context.room_handler().print_in_room(context)
            return

        if payload.get("error"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["error"]))
            return

        context.parameters = [payload["argument"]]
        await context.item_handler().look_item_or_extra(character, context)
        if not context.done:
            context.finish()
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))

    async def do_examine(self, character: Character, context: Context):
        payload = self.info_commands.do_examine(character, context)
        if payload.get("error"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["error"]))
            return

        context.parameters = [payload["argument"]]
        await context.item_handler().look_item_or_extra(character, context)
        if not context.done:
            context.finish()
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            return

        if payload.get("look_in"):
            context.done = False
            context.parameters = ["in", payload["argument"]]
            await context.item_handler().look_in_item(character, context)

    async def do_whois(self, character: Character, context: Context):
        text = self.info_commands.do_whois(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_count(self, character: Character, context: Context):
        text = self.info_commands.do_count(context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_show(self, character: Character, context: Context):
        text = self.info_commands.do_show(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_practice(self, character: Character, context: Context):
        payload = self.info_commands.do_practice(character, context)
        if payload is None:
            return
        if isinstance(payload, str):
            if payload:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload))
            return
        if payload.get("to_char"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["to_char"]))
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)

    async def do_prompt(self, character: Character, context: Context):
        text = self.info_commands.do_prompt(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_equipment(self, character: Character, context: Context):
        text = self.info_commands.do_equipment(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_compare(self, character: Character, context: Context):
        text = self.info_commands.do_compare(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_north(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_north(character, context))

    async def do_east(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_east(character, context))

    async def do_south(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_south(character, context))

    async def do_west(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_west(character, context))

    async def do_up(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_up(character, context))

    async def do_down(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_down(character, context))

    async def do_open(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_open(character, context))

    async def do_close(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_close(character, context))

    async def do_lock(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_lock(character, context))

    async def do_unlock(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_unlock(character, context))

    async def do_pick(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_pick(character, context))

    async def do_stand(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_stand(character, context))

    async def do_rest(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_rest(character, context))

    async def do_sit(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_sit(character, context))

    async def do_sleep(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_sleep(character, context))

    async def do_wake(self, character: Character, context: Context):
        payload = self.movement_commands.do_wake(character, context)
        if payload.get("self_stand"):
            await self.do_stand(character, context)
            return
        await self._handle_room_action_payload(character, context, payload)

    async def do_sneak(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_sneak(character, context))

    async def do_hide(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_hide(character, context))

    async def do_visible(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_visible(character, context))

    async def do_recall(self, character: Character, context: Context):
        await self._handle_move_payload(character, context, self.movement_commands.do_recall(character, context))

    async def do_train(self, character: Character, context: Context):
        await self._handle_room_action_payload(character, context, self.movement_commands.do_train(character, context))

    async def do_wiz_command(self, character: Character, context: Context):
        payload = self.wiz_commands.execute(character, context)
        if isinstance(payload, dict) and payload.get("interpret_at"):
            await self._handle_at_payload(character, context, payload)
            return
        viewer = getattr(payload, "get", lambda *_args, **_kwargs: getattr(context, "character", character))("view_character", getattr(context, "character", character))
        await self._handle_standard_command_payload(viewer, context, payload)

    async def _handle_at_payload(self, character: Character, context: Context, payload: dict):
        try:
            await self._interpret_nested_command(character, context, str(payload.get("interpret_at", "") or ""))
        finally:
            if self._character_in_any_room(character):
                self._restore_at_character(character, payload.get("at_original_room"), payload.get("at_on"))

    async def _interpret_nested_command(self, character: Character, context: Context, raw_command: str):
        cmd, parameters = InterpUtil.extract_parameters(self.interp_registry, raw_command)
        if cmd is None:
            social = self.social_registry.get_or_none(name=raw_command.lower())
            if social is not None and context.social_handler() is not None:
                await context.social_handler().handle_social(character, raw_command, social)
                return
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Huh?\r\n"))
            return

        nested_context = Context(
            character=character,
            handler_service=context.handler_service,
            conn=context.conn,
            command=cmd,
            parameters=InterpUtil.build_arguments(cmd, parameters),
            result=parameters,
            room=self.room_registry.get_or_none(id=character.room_id),
        )
        await self._execute_nested_lambdas(cmd, nested_context)

    async def _execute_nested_lambdas(self, command, context: Context):
        lambdas = getattr(command, "lambdas", None) or []
        if not command.pipeline:
            for lambda_string in lambdas:
                if not isinstance(lambda_string, str) or not lambda_string.strip():
                    continue
                await self._execute_nested_lambda(eval(lambda_string), context)
            return

        index = 0
        while index < len(lambdas):
            lambda_string = lambdas[index]
            if not isinstance(lambda_string, str) or not lambda_string.strip():
                index += 1
                continue
            await self._execute_nested_lambda(eval(lambda_string), context)
            if context.done:
                break
            if isinstance(context.next_index, int) and context.next_index >= 0:
                index = context.next_index
                context.next_index = None
                continue
            index += 1

    @staticmethod
    async def _execute_nested_lambda(func, context: Context):
        if not callable(func):
            return
        result = func(context)
        if inspect.isawaitable(result):
            context.result = await result
        else:
            context.result = result

    def _character_in_any_room(self, character: Character) -> bool:
        character_id = str(getattr(character, "id", "") or "")
        if not character_id:
            return False
        for room in self.room_registry.all_rooms():
            if character_id in getattr(room, "characters", {}) or character_id in getattr(room, "mobiles", {}):
                return True
        return False

    def _restore_at_character(self, character: Character, original_room, original_on):
        if original_room is None:
            return
        character_id = str(getattr(character, "id", "") or "")
        for room in self.room_registry.all_rooms():
            if character_id in getattr(room, "characters", {}):
                room.remove_player_from_room(character)
            if character_id in getattr(room, "mobiles", {}):
                room.remove_mobile_from_room(character)
        if CharacterApi.is_npc(character):
            original_room.add_mobile_to_room(character)
        else:
            original_room.add_player_to_room(character)
        character.room_id = original_room.id
        character.area_id = original_room.area_id
        setattr(character, "on", original_on)

    async def do_object_command(self, character: Character, context: Context):
        payload = self.object_commands.execute(character, context)
        if payload is None:
            return
        if isinstance(payload, str):
            if payload:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload))
            return
        if payload.get("payloads"):
            await self._emit_standard_payloads(character, payload.get("payloads", []), context=context)
            return
        await self._emit_standard_payload(character, payload)

    async def do_communications_command(self, character: Character, context: Context):
        payload = self.communications_commands.execute(context)
        if payload is None:
            return
        if isinstance(payload, str):
            if payload:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload))
            return
        if payload.get("ordered_commands"):
            await self._handle_order_payload(character, context, payload)
            return
        if payload.get("payloads"):
            await self._emit_standard_payloads(character, payload.get("payloads", []), context=context)
            return
        await self._emit_standard_payload(character, payload)
        if payload.get("to_area"):
            await self.message_bus.send_to_area(character.area_id, self.message_bus.text_to_message(payload["to_area"]))
        if payload.get("to_world"):
            await self.message_bus.broadcast(self.message_bus.text_to_message(payload["to_world"]), [character.id])
        if payload.get("global_message"):
            targets = payload.get("global_targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["global_message"]), targets)
        if payload.get("broadcast_message"):
            exclude_ids = payload.get("exclude_character_ids", [])
            await self.message_bus.broadcast(self.message_bus.text_to_message(payload["broadcast_message"]), exclude_ids)

    async def _handle_order_payload(self, character: Character, context: Context, payload: dict):
        message_key = str(payload.get("order_message_key", "") or "ordered")
        for entry in payload.get("ordered_commands", []):
            victim = entry.get("victim")
            command_text = str(entry.get("command", "") or "")
            if victim is None or not command_text:
                continue
            order_payload = self.interp_api.render_message_key(
                context,
                message_key,
                channel="to_victim",
                s=command_text,
                t=getattr(victim, "name", ""),
            )
            if order_payload.get("to_victim"):
                await self.message_bus.send_to_character(victim.id, self.message_bus.text_to_message(order_payload["to_victim"]))
            await self._interpret_nested_command(victim, context, command_text)
        if payload.get("to_char"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["to_char"]))

    async def do_hit(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_kill(character, context))

    async def do_kill(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_kill(character, context))

    async def do_cast(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_cast(character, context))

    async def do_backstab(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_backstab(character, context))

    async def do_bash(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_bash(character, context))

    async def do_berserk(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_berserk(character, context))

    async def do_dirt(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_dirt(character, context))

    async def do_disarm(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_disarm(character, context))

    async def do_flee(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_flee(character, context))

    async def do_kick(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_kick(character, context))

    async def do_murde(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_murde(character, context))

    async def do_murder(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_murder(character, context))

    async def do_rescue(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_rescue(character, context))

    async def do_trip(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.do_trip(character, context))

    async def do_fight_command(self, character: Character, context: Context):
        await self._handle_fight_payload(character, context, self.fight_commands.execute(character, context))

    async def _handle_fight_payload(self, character: Character, context: Context, payload):
        if payload is None:
            return
        if isinstance(payload, str):
            if payload:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload))
            return
        payloads = payload.get("payloads")
        if payloads:
            await self._emit_standard_payloads(character, payloads, context=context)
            return
        await self._emit_standard_payloads(character, [payload], context=context)

    async def _send_prompt(self, character: Character, context: Context, prefer_context_room: bool = True):
        room = context.room if prefer_context_room and context is not None and context.room is not None else None
        if room is None:
            room_registry = getattr(self, "room_registry", None)
            if room_registry is None:
                return
            room = room_registry.get_or_none(id=getattr(character, "room_id", ""))
        if room is None:
            return
        area_id = getattr(room, "area_id", getattr(character, "area_id", ""))
        area_registry = getattr(self, "area_registry", None)
        area = area_registry.get_or_none(id=area_id) if area_id and area_registry is not None else None
        if area is None:
            return
        await self.message_bus.send_prompt(character, area, room)

    async def print_players_in_room(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return
        message = room.get_players_in_room(character)
        if message:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    async def to_player(self, character_id, msg: str):
        text = msg + "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    async def to_target(self, context: Context):
        target = self.character_registry.get_or_none(name=context.parameters[0])
        if target is None:
            await self.message_bus.send_to_character(context.character.id,
                                                     self.message_bus.text_to_message("They aren't here.\r\n"))
            return
        text = context.parameters[1] + "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(target.id, message)

    async def to_room(self, character: Character, msg: str):
        room = self.room_registry.get(id=character.room_id)
        text = msg.replace("%c", character.name).replace("%m", msg)
        message = self.message_bus.text_to_message(text)
        in_room = room.player_targets(character)
        await self.message_bus.send_to_room(message, in_room)

    async def look_target(self, character: Any, context: Context):
        text = self.info_commands.look_target(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def check_position(self, character: Character) -> bool:
        positions = CharacterApi.get_enum('positions')
        current_position = getattr(getattr(character, "character_attributes", None), "position", None)
        if current_position is None:
            return True

        if current_position < positions.POS_SLEEPING.value:
            await self.message_bus.send_to_character(
                character.id,
                self.message_bus.text_to_message("You can't see anything but stars!\n\r"),
            )
            return False

        if current_position == positions.POS_SLEEPING.value:
            await self.message_bus.send_to_character(
                character.id,
                self.message_bus.text_to_message("You can't see anything; you're sleeping!\n\r"),
            )
            return False

        return True

    async def _handle_room_action_payload(self, character: Character, context: Context, payload):
        await self._handle_standard_command_payload(character, context, payload)

    async def _handle_standard_command_payload(self, character: Character, context: Context, payload):
        if payload is None:
            return
        if isinstance(payload, str):
            if payload:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload))
            return
        payloads = payload.get("payloads")
        if payloads:
            await self._emit_standard_payloads(character, payloads, context=context)
            return
        await self._emit_standard_payload(character, payload, context=context)

    async def _emit_standard_payload(self, character: Character, payload: dict, context: Context | None = None, prompt_victims: bool = True) -> list[Character]:
        prompt_targets: list[Character] = []
        payload = self._resolve_standard_payload(character, payload, context=context)
        if isinstance(payload, dict):
            payload["to_char"] = f"{payload.get('to_char', '')}{Ability.take_improve_messages(character)}"
            victim = payload.get("victim")
            if victim is not None:
                payload["to_victim"] = f"{payload.get('to_victim', '')}{Ability.take_improve_messages(victim)}"
        if payload.get("to_char"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["to_char"]))
        if payload.get("to_victim") and payload.get("victim") is not None:
            victim = payload["victim"]
            await self.message_bus.send_to_character(victim.id, self.message_bus.text_to_message(payload["to_victim"]))
            if victim is not character and not CharacterApi.is_npc(victim):
                if prompt_victims:
                    await self._send_prompt(victim, context, prefer_context_room=False)
                else:
                    prompt_targets.append(victim)
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
        if payload.get("to_wiznet"):
            actor = payload.get("wiznet_actor", context.character if context is not None else character)
            targets = self.wiz_handler.wiznet_targets(
                actor,
                flag_name=str(payload.get("wiznet_flag", "") or ""),
                skip_flag_name=str(payload.get("wiznet_skip_flag", "") or ""),
                min_level=GenericUtil.to_int(payload.get("wiznet_min_level", 0), 0),
            )
            for target in targets:
                text = self.wiz_handler.decorate_wiznet_text(target, payload["to_wiznet"])
                await self.message_bus.send_to_character(target.id, self.message_bus.text_to_message(text))
        if payload.get("room_message"):
            targets = payload.get("room_targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["room_message"]), targets)
        if payload.get("global_message"):
            targets = payload.get("global_targets", [])
            if len(targets) > 0:
                if isinstance(targets[0], str):
                    for target_id in targets:
                        await self.message_bus.send_to_character(target_id, self.message_bus.text_to_message(payload["global_message"]))
                else:
                    await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["global_message"]), targets)
        if payload.get("broadcast_message"):
            exclude_ids = payload.get("exclude_character_ids", [])
            await self.message_bus.broadcast(self.message_bus.text_to_message(payload["broadcast_message"]), exclude_ids)
        for target in payload.get("target_messages", []):
            target_id = str(target.get("id", "") or "")
            text = str(target.get("text", "") or "")
            if target_id and text:
                await self.message_bus.send_to_character(target_id, self.message_bus.text_to_message(text))
        if payload.get("disconnect_character") is not None:
            session = self.wiz_handler.current_session(payload["disconnect_character"])
            connection = None if session is None else self.message_bus.connection_manager.get_connection(session.session_id)
            if connection is not None:
                await connection.close()
        if context is not None:
            if payload.get("from_room_message"):
                targets = payload.get("from_room_targets", [])
                if len(targets) > 0:
                    await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["from_room_message"]), targets)
            if payload.get("to_room_message"):
                targets = payload.get("to_room_targets", [])
                if len(targets) > 0:
                    await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room_message"]), targets)
            to_room = payload.get("to_room_obj")
            if to_room is not None:
                viewer = payload.get("view_character", character)
                await self._show_room_to_character(viewer, to_room, context)
                if viewer is character:
                    prompted_characters: dict[str, Character] = {}
                    for attacker, fight_payload in payload.get("aggressive_rounds", []):
                        prompted = await self.fight_handler.emit_round_payload(attacker, fight_payload)
                        prompted_characters.update({target.id: target for target in prompted})
                    for target in prompted_characters.values():
                        await self._send_prompt(target, context, prefer_context_room=False)
        return prompt_targets

    async def _emit_standard_payloads(self, character: Character, payloads: list[dict], context: Context | None = None):
        prompt_targets: dict[str, Character] = {}
        for payload in payloads:
            for target in await self._emit_standard_payload(character, payload, context=context, prompt_victims=False):
                prompt_targets[str(getattr(target, "id", id(target)))] = target
        for target in prompt_targets.values():
            await self._send_prompt(target, context, prefer_context_room=False)

    def _resolve_standard_payload(self, character: Character, payload, context: Context | None = None):
        if not isinstance(payload, dict) or context is None:
            return payload

        command = getattr(context, "command", None)
        message_key = str(payload.get("message_key", "") or "").strip()
        if command is None or not message_key:
            return payload

        token_factory = payload.get("token_factory")
        tokens: dict[str, Any] = {}
        if callable(token_factory):
            tokens.update(dict(token_factory(character=character, context=context, payload=payload) or {}))
        tokens.update(dict(payload.get("tokens", {}) or {}))

        rendered = {
            key: value
            for key, value in payload.items()
            if key not in {"message_key", "token_factory", "tokens", "channel", "fallback"}
        }
        fallback = str(payload.get("fallback", "") or "")
        for channel in self._payload_channels_for_message(getattr(command, "payload", None), message_key, channel=str(payload.get("channel", "") or "")):
            rendered.update(self.interp_api.render_message_key(context, message_key, channel=channel, fallback=fallback, **tokens))
        return rendered

    @staticmethod
    def _payload_channels_for_message(payload_def, message_key: str, channel: str = "") -> list[str]:
        if channel:
            return [channel]
        if payload_def is None:
            return []

        channels: list[str] = []
        for field_info in fields(payload_def):
            field_name = str(field_info.name)
            table = getattr(payload_def, field_name, {}) or {}
            if message_key in table:
                channels.append(field_name)
        return channels

    async def _show_room_to_character(self, viewer: Character, room, context: Context):
        if viewer is None:
            return
        await context.room_handler().print_room(viewer.id, room)
        autoexit_bit = None
        if self.info_commands.PlayerActBits is not None:
            autoexit_bit = self.info_commands.PlayerActBits.PLR_AUTOEXIT.value
        if autoexit_bit is not None:
            act = viewer.status_flags.act
            if CharacterApi.is_set(act, autoexit_bit):
                await context.room_handler().print_exits(viewer)
        await self.print_players_in_room(viewer)
        await context.mobile_handler().print_mobiles_in_room(viewer)

    async def _handle_move_payload(self, character: Character, context: Context, payload: dict):
        await self._handle_standard_command_payload(character, context, payload)

from typing import Any

from api.CharacterApi import CharacterApi
from api.CommunicationsApi import CommunicationsApi
from interp.Context import Context
from interp.InterpView import InterpView
from util.CommunicationsUtil import CommunicationsUtil
from util.DisplayUtil import DisplayUtil
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil


class MoneyApi:
    @classmethod
    def split_amounts(cls, view: InterpView) -> dict[str, int]:
        silver_text, rest = CommunicationsUtil.split_first(InterpUtil.argument_text(view))
        gold_text, _extra = CommunicationsUtil.split_first(rest)
        return {
            "silver": GenericUtil.to_int(silver_text, 0),
            "gold": GenericUtil.to_int(gold_text, 0) if gold_text else 0,
        }

    @classmethod
    def split_missing_amount(cls, view: InterpView) -> bool:
        first, _rest = CommunicationsUtil.split_first(InterpUtil.argument_text(view))
        return not first

    @classmethod
    def split_negative(cls, view: InterpView) -> bool:
        amounts = cls.split_amounts(view)
        return amounts["silver"] < 0 or amounts["gold"] < 0

    @classmethod
    def split_zero(cls, view: InterpView) -> bool:
        amounts = cls.split_amounts(view)
        return amounts["silver"] == 0 and amounts["gold"] == 0

    @classmethod
    def split_insufficient_funds(cls, view: InterpView) -> bool:
        amounts = cls.split_amounts(view)
        actor = view.context.character
        return GenericUtil.to_int(getattr(actor, "silver", 0), 0) < amounts["silver"] or GenericUtil.to_int(getattr(actor, "gold", 0), 0) < amounts["gold"]

    @classmethod
    def split_members(cls, view: InterpView) -> list[Any]:
        actor = view.context.character
        return [
            candidate
            for candidate in CommunicationsApi.room_people(view)
            if CharacterApi.is_same_group(candidate, actor) and not CommunicationsApi.is_charmed(candidate)
        ]

    @classmethod
    def split_too_few_members(cls, view: InterpView) -> bool:
        return len(cls.split_members(view)) < 2

    @classmethod
    def split_shares(cls, view: InterpView) -> dict[str, int]:
        amounts = cls.split_amounts(view)
        members = max(1, len(cls.split_members(view)))
        return {
            "silver": amounts["silver"] // members,
            "gold": amounts["gold"] // members,
            "extra_silver": amounts["silver"] % members,
            "extra_gold": amounts["gold"] % members,
        }

    @classmethod
    def split_share_zero(cls, view: InterpView) -> bool:
        shares = cls.split_shares(view)
        return shares["silver"] == 0 and shares["gold"] == 0

    @classmethod
    def split_money(cls, context: Context, interp_api):
        view = interp_api.build_interp_view(context)
        payload = interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload

        character = context.character
        amounts = cls.split_amounts(view)
        shares = cls.split_shares(view)
        members = cls.split_members(view)

        character.silver = GenericUtil.to_int(getattr(character, "silver", 0), 0) - amounts["silver"] + shares["silver"] + shares["extra_silver"]
        character.gold = GenericUtil.to_int(getattr(character, "gold", 0), 0) - amounts["gold"] + shares["gold"] + shares["extra_gold"]

        to_char = ""
        if shares["silver"] > 0:
            to_char += interp_api.render_message_key(
                context,
                "split_silver_coins_share",
                channel="to_char",
                amount_silver=amounts["silver"],
                share_silver=shares["silver"] + shares["extra_silver"],
            ).get("to_char", "")
        if shares["gold"] > 0:
            to_char += interp_api.render_message_key(
                context,
                "split_gold_coins_share",
                channel="to_char",
                amount_gold=amounts["gold"],
                share_gold=shares["gold"] + shares["extra_gold"],
            ).get("to_char", "")

        victim_message_key = "split_silver_victim"
        if shares["gold"] > 0 and shares["silver"] == 0:
            victim_message_key = "split_gold_victim"
        elif shares["gold"] > 0 and shares["silver"] > 0:
            victim_message_key = "split_both_victim"

        target_messages = []
        room = CommunicationsApi.current_room(view)
        resting = CharacterApi.pos_value("POS_RESTING")
        for member in members:
            if member == character:
                continue
            member.gold = GenericUtil.to_int(getattr(member, "gold", 0), 0) + shares["gold"]
            member.silver = GenericUtil.to_int(getattr(member, "silver", 0), 0) + shares["silver"]
            if CharacterApi.position_value(member) < resting:
                continue
            sender = DisplayUtil.visible_tokens({"c": character}, member, room)["c"]
            sender = sender[:1].upper() + sender[1:]
            target_messages.append({
                "id": getattr(member, "id", ""),
                "text": interp_api.render_message_key(
                    context,
                    victim_message_key,
                    channel="to_victim",
                    c=sender,
                    amount_silver=amounts["silver"],
                    amount_gold=amounts["gold"],
                    share_silver=shares["silver"],
                    share_gold=shares["gold"],
                ).get("to_victim", ""),
            })

        context.finish()
        return {"to_char": to_char, "target_messages": target_messages}

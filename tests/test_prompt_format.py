import unittest

from interp.PromptFormat import PromptFormat
from server.session.SessionState import SessionStatus


class StubCharacter:
    def __init__(self):
        self.hp = 10
        self.max_hp = 20
        self.mana = 30
        self.max_mana = 40
        self.move = 50
        self.max_move = 60
        self.exp = 70
        self.exp_to_level = 80
        self.gold = 90
        self.silver = 100
        self.alignment = 250
        self.health = 10
        self.movement = 50
        self._immortal = False

    def is_immortal(self):
        return self._immortal


class StubRoom:
    def __init__(self, name="The Test Room", vnum=1234, exits="North, East, South, West"):
        self.name = name
        self.vnum = vnum
        self._exits = exits

    def get_formatted_exits(self):
        return self._exits


class StubArea:
    def __init__(self, name="The Test Area"):
        self.name = name


class TestPromptFormat(unittest.TestCase):

    def setUp(self):
        self.prompt = PromptFormat(
            hp=True,
            max_hp=True,
            mana=True,
            max_mana=True,
            movement=True,
            max_movement=True,
            xp=True,
            max_xp=True,
            gold=True,
            silver=True,
            alignment=True
        )
        self.character = StubCharacter()
        self.room = StubRoom()
        self.area = StubArea()

    def test_default_prompt_format(self):
        default_prompt = PromptFormat.default()
        self.assertTrue(default_prompt.hp)
        self.assertFalse(default_prompt.max_hp)
        self.assertTrue(default_prompt.movement)
        self.assertFalse(default_prompt.max_movement)
        self.assertTrue(default_prompt.mana)
        self.assertFalse(default_prompt.max_mana)

    def test_from_template_sets_fields(self):
        prompt = PromptFormat.from_template("<%h/%H %m/%M %v/%V %x/%X %g %s %a %r %e %R %z%c>")
        self.assertTrue(prompt.hp)
        self.assertTrue(prompt.max_hp)
        self.assertTrue(prompt.mana)
        self.assertTrue(prompt.max_mana)
        self.assertTrue(prompt.movement)
        self.assertTrue(prompt.max_movement)
        self.assertTrue(prompt.xp)
        self.assertTrue(prompt.max_xp)
        self.assertTrue(prompt.gold)
        self.assertTrue(prompt.silver)
        self.assertTrue(prompt.alignment)
        self.assertTrue(prompt.room_name)
        self.assertTrue(prompt.exits)
        self.assertTrue(prompt.room_vnum)
        self.assertTrue(prompt.area_name)
        self.assertTrue(prompt.carriage_return)

    def test_to_json(self):
        prompt = PromptFormat.from_template("<%h %m %v>")
        data = prompt.to_json()
        self.assertTrue(data["hp"])
        self.assertTrue(data["mana"])
        self.assertTrue(data["movement"])
        self.assertFalse(data["gold"])

    def test_call_prompt_lambda_zero_arg(self):
        fn = lambda: "\n"
        result = PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertEqual("\n", result)

    def test_call_prompt_lambda_single_character_arg(self):
        fn = lambda c: c.hp
        result = PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertEqual(10, result)

    def test_call_prompt_lambda_single_room_arg(self):
        fn = lambda r: r.name if r and r.name else ""
        result = PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertEqual("The Test Room", result)

    def test_call_prompt_lambda_single_area_arg(self):
        fn = lambda a: a.name if a and a.name else ""
        result = PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertEqual("The Test Area", result)

    def test_call_prompt_lambda_two_arg_character_room(self):
        self.character._immortal = True
        fn = lambda c, r: r.vnum if c.is_immortal() and r else ""
        result = PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertEqual(1234, result)

    def test_call_prompt_lambda_two_arg_character_area(self):
        self.character._immortal = True
        fn = lambda c, a: a.name if c.is_immortal() and a else ""
        result = PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertEqual("The Test Area", result)

    def test_call_prompt_lambda_invalid_single_arg_name_raises(self):
        fn = lambda x: x
        with self.assertRaises(ValueError) as ctx:
            PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertIn("Unsupported single-arg lambda parameter", str(ctx.exception))

    def test_call_prompt_lambda_invalid_two_arg_names_raises(self):
        fn = lambda r, a: ""
        with self.assertRaises(ValueError) as ctx:
            PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertIn("Unsupported two-arg lambda parameters", str(ctx.exception))

    def test_call_prompt_lambda_invalid_arity_raises(self):
        fn = lambda c, r, a: ""
        with self.assertRaises(ValueError) as ctx:
            PromptFormat._call_prompt_lambda(fn, self.character, self.room, self.area)
        self.assertIn("Unsupported lambda arity", str(ctx.exception))

    def test_render_prompt_uses_internal_fields(self):
        self.character._immortal = True
        prompt = PromptFormat.from_template("<%h/%H %m/%M %v/%V %x/%X %g %s %a %r %e %R %z%c>")
        result = prompt.render_prompt(SessionStatus.PLAYING, self.character, self.room, self.area)

        expected = "<10/20 30/40 50/60 70/80 90 100 250 The Test Room North, East, South, West 1234 The Test Area>\n"
        self.assertEqual(expected, result.data["text"])

    def test_render_prompt_while_afk(self):
        self.character._immortal = True
        prompt = PromptFormat.from_template("<%h/%H %m/%M %v/%V %x/%X %g %s %a %r %e %R %z%c>")
        result = prompt.render_prompt(SessionStatus.IDLING, self.character, self.room, self.area)

        expected = "<AFK><10/20 30/40 50/60 70/80 90 100 250 The Test Room North, East, South, West 1234 The Test Area>\n"
        self.assertEqual(expected, result.data["text"])

    def test_render_prompt_with_missing_room_and_area(self):
        self.character._immortal = True
        prompt = PromptFormat.from_template("<%r %e %R %z>")
        result = prompt.render_prompt(SessionStatus.PLAYING, self.character, None, None)
        self.assertEqual("<   >", result.data["text"])


if __name__ == "__main__":
    unittest.main()
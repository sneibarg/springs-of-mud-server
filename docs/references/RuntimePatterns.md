# Low-Code Runtime Patterns

- Commands come from `SOMDB.Commands.json` and become `interp.Command` objects. They may define `lambdas`, `guards`, `payload`, `pipeline`, and metadata such as role, position, usage, and level.
- Skills and spells share `skill.Ability`. They normalize collection JSON into payloads, guards, class level/rating maps, handler IDs, targets, beats, mana, and effect data.
- Guard definitions are data-driven lambda strings compiled by `InterpApi` or `FightApi`. Prefer adding safe helper functions to API/util classes over embedding complex logic in collection lambdas.
- Payloads should flow through `GamePayload`, `PayloadUtil`, `InterpApi.render_message_key`, and `MessageBus`. Use `to_char`, `to_victim`, `to_room`, `to_area`, `to_world`, and `to_wiznet` payload channels instead of writing directly to connections.
- Fight actions use `game.action.ActionDefinition`, `ActionGuard`, `ActionPlan`, and `MessageRef`. Skill documents can provide `fightExecutor`, `fightPlan`, and guards; Python should provide reusable executors or helpers.
- Spell lambdas execute through `SpellApi` and `SpellContext`. Add reusable spell operations to `SpellApi` when designer-authored spell data needs a new primitive.
- Effects are runtime state, but their user-facing payloads belong to the skill or spell document that created or owns the effect. Periodic effect ticks such as plague, poison, or object affect expiration should render message keys from the appropriate `SOMDB.Skills.json` or `SOMDB.Spells.json` payload instead of hard-coding text in `UpdateHandler` or effect utilities.

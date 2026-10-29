# Self-skill activation

Skill documents can define `activation` for a self-targeted proficiency attempt.
The runtime `SkillApi.activate(character, skill, effect_handler)` prepares the
actor, rolls `number_percent() < effective proficiency`, records improvement,
and applies successful effects. The movement handlers currently use this for
sneak and hide. No wait or mana cost is implicit in this operation.

Supported fields:

| Field | Behavior |
| --- | --- |
| `stripType` | Remove existing effects with this type before rolling |
| `clearFlag` | Clear this affected-by flag before rolling |
| `skipIfFlag` | Skip the roll and improvement if this flag remains after preparation |
| `improveMultiplier` | Improvement difficulty multiplier; defaults to 1 |
| `successFlag` | Set this affected-by flag on success |
| `affects` | Standard effect documents to apply to the actor on success |

Effect level, duration and modifier support the existing numeric expressions
using `level`. Set an explicit skill effect type, such as `skill.sneak`, so the
effect's expiry text resolves back to the owning skill payload. Effects are
removed through the ordinary effect lifecycle. The command document continues
to own the immediate attempt message.

For example, sneak strips `skill.sneak`, skips an attempt if an innate AFF_SNEAK
remains, and otherwise applies a level-duration AFF_SNEAK effect after a
successful roll. Hide clears AFF_HIDE before attempting to set it again.

# Runtime entity factories

Use `item.ItemFactory.ItemFactory` and `mobile.MobileFactory.MobileFactory` to
construct live entities. The factories are stateless; they require no container
binding or lazy-load setup. Mobile creation receives its runtime enum provider
explicitly.

- `ItemFactory.create(prototype)` creates an empty item with a new identity and
  independent effects. It does not copy room ownership or contained items, and
  retains the existing light and jukebox spawn initialization.
- `ItemFactory.copy_instance(item)` copies current values, enchantment state,
  effects, and nested contents, assigning new identities throughout the tree.
- `MobileFactory.create(prototype, enum_provider)` runs the existing mobile spawn
  rules, including stat initialization, randomized resources and wealth, and
  independent armor/status state.
- `MobileFactory.copy_instance(mobile, enum_provider)` uses those spawn rules and
  copies the source's descriptive fields, currency, flags, and possessions. It
  preserves equipment placement and copies each owned item once. This operation
  is not a persistence snapshot: it does not duplicate active combat or arbitrary
  temporary runtime attributes.

`ItemFactory.from_data(document, liquids, ability_registries)` and
`MobileFactory.from_data(document, races)` own prototype construction for the
content services. They preserve service identities and use the existing
normalization and model `from_json` contracts; they do not run spawn rules.
Normalization helpers now live on the respective factories.

The former `ItemUtil.create_object`, `ItemUtil.clone_object_instance`,
`MobileUtil.create_mobile`, and `MobileUtil.clone_mobile_instance` methods have
been removed. Runtime callers and active regression tests use the factories.

## Gameplay ownership

`ItemUtil` and `MobileUtil` have been removed entirely. Their remaining
responsibilities are owned by:

- `ItemApi`: item visibility, newbie-pit identification, sacrifice reward values,
  and pure lookup of the entity using an item.
- `MobileApi`: trainer eligibility and existing collection-facing mobile actions.
- `Item` and `Room`: item descriptions, grouping/counting, and room item lines.
- `AnimateEntity` and `Equipped`: inventory and equipment mutations.
- `ItemOwnership`: world-item traversal and vnum lookup, including location kind.
- `InterpUtil`: object-command argument parsing.
- `StatusFlags`: removal of named flag domains using its guarded mutation methods.

The `get`, `take`, `pour`, and `sacrifice` command documents use these contracts.
The interpreter no longer exposes either removed utility. Sacrifice prepares
occupant tokens explicitly before checking its guards; automatic sacrifice
renders the command's live payload with bundled command data as a fallback.

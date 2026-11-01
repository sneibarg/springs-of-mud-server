# Collection Data

Use `$collection-query` before inspecting or editing `resources/collections/*.json`. That skill explains how to query collection snapshots through `python -m src.devtools` without dumping large JSON files into context.

Read a whole collection only when `$collection-query` cannot answer the question or when exact edit context is required. After editing a collection, use the skill again to verify the changed document.

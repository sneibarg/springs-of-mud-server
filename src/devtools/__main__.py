import sys

from .collection_query import main as query_main


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "modify":
        from .collection_modify import main as modify_main

        raise SystemExit(modify_main(sys.argv[2:]))
    raise SystemExit(query_main())

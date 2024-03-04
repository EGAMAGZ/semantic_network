from ui import display_graph
from util.file import (
    get_objects_table,
    get_semantic_table,
)
from util.mermaid import ObjectsTable, SemanticNetwork


def main() -> None:

    objects_table: ObjectsTable = get_objects_table()

    semantic_network: SemanticNetwork = get_semantic_table()

    display_graph(objects_table, semantic_network)


if __name__ == "__main__":
    main()

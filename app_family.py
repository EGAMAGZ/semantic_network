from ui import display_graph
from util.file import register_objects_csv, register_semantic_csv
from util.mermaid import ObjectsTable, SemanticNetwork
from util.text import divide_text
from itertools import groupby


def main() -> None:
    with open("data/info.txt") as file:
        content: str = file.read().replace("\n", "")
    sentences: list[str] = content.split(".")

    objects_table: ObjectsTable = {}
    total_objects: int = 0

    number_row = 0
    semantic_network: SemanticNetwork = {}

    words_index: dict[str, int] = {}

    for sentence in sentences:
        if not sentence:
            continue

        clean_sentence = sentence.strip()

        group_1, group_2, group_3 = divide_text(clean_sentence)

        for object_1 in group_1:
            for object_2 in group_2:
                for object_3 in group_3:

                    if object_1 not in objects_table.values():
                        total_objects += 1
                        objects_table[total_objects] = object_1
                        words_index[object_1] = total_objects

                    if object_2 not in objects_table.values():
                        total_objects += 1
                        objects_table[total_objects] = object_2
                        words_index[object_2] = total_objects

                    if object_3 not in objects_table.values():
                        total_objects += 1
                        objects_table[total_objects] = object_3
                        words_index[object_3] = total_objects

                    semantic_network[number_row] = (
                        words_index[object_1],
                        words_index[object_2],
                        words_index[object_3],
                    )
                    number_row += 1

    groups_by_relation: dict[int, list[tuple[int, int, int]]] = {
        key: list(value)
        for key, value in groupby(semantic_network.values(), key=lambda x: x[1])
    }
    for key, value in groups_by_relation.items():
        # Prolog
        for b in value:
            print(
                f"{objects_table.get(b[1])[0]}({objects_table.get(b[0])[0]},{objects_table.get(b[2])})."
            )


if __name__ == "__main__":
    main()

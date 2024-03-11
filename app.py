from ui import display_graph
from util.file import register_objects_csv, register_semantic_csv
from util.mermaid import ObjectsTable, SemanticNetwork
from util.text import TextInfo, divide_text


def main() -> None:
    with open("data/info.txt") as file:
        content: str = file.read().replace("\n", "")
    sentences: list[str] = content.split(".")

    objects_table: ObjectsTable = {}
    total_objects: int = 0

    number_row = 0
    semantic_network: SemanticNetwork = {}

    words_index: dict[TextInfo, int] = {}

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

    register_semantic_csv(semantic_network)
    register_objects_csv(objects_table)
    display_graph(objects_table, semantic_network)



if __name__ == "__main__":
    main()

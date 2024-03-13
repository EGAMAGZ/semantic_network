import re
from typing import Literal
from ui import display_graph

from util.mermaid import ObjectsTable, SemanticNetwork


def main() -> None:

    with open("data/family.txt") as file:
        content: str = file.read().replace("\n", "")
    sentences: list[str] = content.split(".")

    number_row_table = 0
    number_row_network = 0
    object_table: ObjectsTable = {}
    words_index: dict[str, int] = {}
    semantic_network: SemanticNetwork = {}

    group_1: list[str] = []
    group_2: list[str] = []
    group_3: list[str] = []

    for sentence in sentences:
        if not sentence:
            continue

        is_group_3 = False
        group_1 = []
        group_2 = []
        group_3 = []

        type_sentence: Literal["R", "O"] | None = None
        current_word = ""
        clean_sentence = sentence.strip()

        for character in clean_sentence:
            if character == "(":
                type_sentence = "O"

            if character == "[":
                is_group_3 = True
                type_sentence = "R"

            if type_sentence:
                current_word += character

            if character == ")" or character == "]":
                if type_sentence == "R":
                    group_2.append(re.sub(r"[\[\]\(\)]", "", current_word))

                if type_sentence == "O" and is_group_3:
                    group_3.append(re.sub(r"[\[\]\(\)]", "", current_word))

                if type_sentence == "O" and not is_group_3:
                    group_1.append(re.sub(r"[\[\]\(\)]", "", current_word))

                current_object = (
                    re.sub(r"[\[\]\(\)]", "", current_word),
                    type_sentence,
                )

                if current_object not in object_table.values():
                    number_row_table += 1
                    object_table[number_row_table] = current_object
                    words_index[re.sub(r"[\[\]\(\)]", "", current_word)] = (
                        number_row_table
                    )

                type_sentence = None
                current_word = ""

        for object_1 in group_1:
            for object_2 in group_2:
                for object_3 in group_3:
                    number_row_network += 1
                    semantic_network[number_row_network] = (
                        words_index[object_1],
                        words_index[object_2],
                        words_index[object_3],
                    )

    display_graph(object_table, semantic_network)


if __name__ == "__main__":
    main()

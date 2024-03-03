import re
from webui import webui
from enum import Enum
from typing import Literal
from jinja2 import Environment, FileSystemLoader
from python_mermaid.diagram import Node, Link, MermaidDiagram

type SemanticNetwork = dict[int, tuple[int, int, int]]
type ObjectsTable = dict[int, tuple[str, Literal["R", "O"]]]


class ObjectType(Enum):
    OBJECT = "O"
    RELATION = "R"
    NONE = "N"


def main() -> None:
    with open("entrada.txt") as file:
        content: str = file.read().replace("\n", "")
    sentences: list[str] = content.split(".")

    objects_table: ObjectsTable = {}

    total_objects: int = 0

    current_value: str = ""
    current_object_type: ObjectType = ObjectType.NONE

    for sentence in sentences:
        clean_sentence = sentence.strip()

        for character in clean_sentence:
            if character == "[":
                current_object_type = ObjectType.RELATION

            if character == "(":
                current_object_type = ObjectType.OBJECT

            if current_object_type != ObjectType.NONE:
                current_value += character

            if character == "]" or character == ")":
                current_row = (
                    re.sub(r"[\[\]\(\)]", "", current_value),
                    current_object_type.value,
                )
                if current_row not in objects_table.values():
                    total_objects += 1
                    objects_table[total_objects] = current_row

                current_object_type = ObjectType.NONE
                current_value = ""

    number_row = 0
    semantic_network: SemanticNetwork = {}

    keys = list(objects_table.keys())
    temp_row: list[int | None] = [None, None, None]

    for key, (_, object_type) in objects_table.items():
        current_index = keys.index(key)

        if object_type == "O":
            if temp_row[0] is None:
                temp_row[0] = key
            else:
                if temp_row[2] is None:
                    temp_row[2] = key

        if object_type == "R" and temp_row[1] is None:
            temp_row[1] = key

        if (
            temp_row[0] is not None
            and temp_row[1] is not None
            and temp_row[2] is not None
        ):
            number_row += 1
            semantic_network[number_row] = tuple(temp_row)

            if current_index < len(keys) - 1:
                next_key = keys[current_index + 1]
                next_element = objects_table.get(next_key)

                if object_type == "R":
                    if next_element[1] == "O":
                        temp_row[2] = None

                if object_type == "O":
                    if next_element[1] == "R":
                        temp_row[1] = None
                        temp_row[2] = None

                    if next_element[1] == "O":
                        temp_row[2] = None

    display_graph(objects_table, semantic_network)


def generate_mermaid(
    objects_table: ObjectsTable,
    semantic_network: SemanticNetwork,
) -> str:
    nodes = {
        key: Node(text)
        for key, (text, object_type) in objects_table.items()
        if object_type == "O"
    }
    edges = {
        key: text
        for key, (text, object_type) in objects_table.items()
        if object_type == "R"
    }

    list_links = [
        Link(
            nodes.get(idx_object_1),
            nodes.get(idx_object_2),
            message=edges.get(idx_relation),
        )
        for idx_object_1, idx_relation, idx_object_2 in semantic_network.values()
    ]

    return MermaidDiagram(
        title="Diagrama de Clasificacion de Objetos",
        links=list_links,
        nodes=list(nodes.values()),
    )


def display_graph(
    objects_table: ObjectsTable, semantic_network: SemanticNetwork
) -> None:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    mermaid_code = generate_mermaid(objects_table, semantic_network)
    web_window = webui.window()
    web_window.show(
        template.render(
            mermaid_code=mermaid_code,
            objects_table=objects_table,
            semantic_network=semantic_network,
        ),
    )
    webui.wait()


if __name__ == "__main__":
    main()

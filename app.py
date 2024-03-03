import re
from webui import webui
from rich.console import Console
from rich.table import Table
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

    temp_row: list[int | None] = [None, None, None]
    keys = list(objects_table.keys())
    for key, value in objects_table.items():
        current_index = keys.index(key)

        if value[1] == "O":
            if temp_row[0] is None:
                temp_row[0] = key
            else:
                if temp_row[2] is None:
                    temp_row[2] = key

        if value[1] == "R" and temp_row[1] is None:
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

                if value[1] == "R":
                    if next_element[1] == "O":
                        temp_row[2] = None

                if value[1] == "O":
                    if next_element[1] == "R":
                        temp_row[1] = None
                        temp_row[2] = None

                    if next_element[1] == "O":
                        temp_row[2] = None

    print_tables(objects_table, semantic_network)
    display_graph(objects_table, semantic_network)


def generate_mermaid(
    objects_table: ObjectsTable,
    semantic_network: SemanticNetwork,
) -> str:
    nodes = {
        key: Node(value[0]) for key, value in objects_table.items() if value[1] == "O"
    }
    edges = {key: value[0] for key, value in objects_table.items() if value[1] == "R"}

    list_nodes = [node for node in nodes.values()]
    list_links = [
        Link(nodes.get(value[0]), nodes.get(value[2]), message=edges.get(value[1]))
        for value in semantic_network.values()
    ]

    diagram = MermaidDiagram(
        title="Diagrama de Clasificacion de Objetos",
        links=list_links,
        nodes=list_nodes,
    )
    return diagram


def display_graph(
    objects_table: ObjectsTable, semantic_network: SemanticNetwork
) -> None:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    mermaid_code = generate_mermaid(objects_table, semantic_network)
    web_window = webui.window()
    web_window.show(template.render(mermaid_code=mermaid_code))
    webui.wait()


def print_tables(
    objects_table: ObjectsTable, semantic_network: SemanticNetwork
) -> None:
    console = Console()

    first_table = Table(title="Tabla de Objetos")
    first_table.add_column("Indice")
    first_table.add_column("Texto")
    first_table.add_column("Tipo")

    for key, value in objects_table.items():
        first_table.add_row(
            str(key),
            value[0],
            value[1],
        )

    console.print(first_table)

    second_table = Table(title="Red Semantica")

    second_table.add_column("No.")
    second_table.add_column("Objeto")
    second_table.add_column("Relacion")
    second_table.add_column("Objeto")

    for key, value in semantic_network.items():

        second_table.add_row(str(key), str(value[0]), str(value[1]), str(value[2]))

    console.print(second_table)


if __name__ == "__main__":
    main()

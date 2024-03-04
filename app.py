from webui import webui
from jinja2 import Environment, FileSystemLoader
from python_mermaid.diagram import Node, Link, MermaidDiagram
from util.text import TextInfo, divide_text

type SemanticNetwork = dict[int, tuple[int, int, int]]
type ObjectsTable = dict[int, TextInfo]


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

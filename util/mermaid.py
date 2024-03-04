from python_mermaid.diagram import Node, Link, MermaidDiagram

from util.text import TextInfo

type SemanticNetwork = dict[int, tuple[int, int, int]]

type ObjectsTable = dict[int, TextInfo]


def generate_mermaid(
    objects_table: dict[int, TextInfo],
    semantic_network: dict[int, tuple[int, int, int]],
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

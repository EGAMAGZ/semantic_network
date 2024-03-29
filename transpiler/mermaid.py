from python_mermaid.diagram import Node, Link, MermaidDiagram

from util.type import TextInfo


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

    diagram_code = str(MermaidDiagram(
        links=list_links,
        nodes=list(nodes.values()),
    ))
    return diagram_code

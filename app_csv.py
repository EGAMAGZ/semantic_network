from webui import webui
from jinja2 import Environment, FileSystemLoader
from util.file import (
    get_objects_table,
    get_semantic_table,
)
from util.mermaid import ObjectsTable, SemanticNetwork, generate_mermaid


def main() -> None:

    objects_table: ObjectsTable = get_objects_table()

    semantic_network: SemanticNetwork = get_semantic_table()
    print(semantic_network)

    display_graph(objects_table, semantic_network)


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

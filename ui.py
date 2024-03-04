from webui import webui
from jinja2 import Environment, FileSystemLoader
from util.mermaid import ObjectsTable, SemanticNetwork, generate_mermaid


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

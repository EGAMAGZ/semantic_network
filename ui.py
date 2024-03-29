from webui import webui
from jinja2 import Environment, FileSystemLoader

from transpiler.mermaid import generate_mermaid
from util.type import ObjectsTable, SemanticNetwork


def display_graph(
        objects_table: ObjectsTable, semantic_network: SemanticNetwork
) -> None:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("views/a.html")

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

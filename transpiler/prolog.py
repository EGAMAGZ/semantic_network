from jinja2 import Environment, FileSystemLoader
from util.text import TextInfo
from util.type import SemanticNetwork, ObjectsTable


def to_prolog_syntax(plain_text: str) -> str:
    return plain_text.lower().replace(" ", "_")


def to_prolog_instance(
        relation: TextInfo, object_1: TextInfo, object_2: TextInfo
) -> str:
    return "{0}({1},{2}).".format(
        to_prolog_syntax(relation[0]),
        to_prolog_syntax(object_1[0]),
        to_prolog_syntax(object_2[0]),
    )


def generate_prolog_code(
        semantic_network: SemanticNetwork, objects_table: ObjectsTable
) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("prolog/family.pl")

    list_instances = [
        to_prolog_instance(
            object_1=objects_table[object_1],
            object_2=objects_table[object_2],
            relation=objects_table[relation],
        )
        for object_1, relation, object_2 in semantic_network.values()
    ]

    instances_text = "\n".join(list_instances)
    return template.render(instances=instances_text)
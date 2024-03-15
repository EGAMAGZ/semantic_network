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
    list_instances = [
        to_prolog_instance(
            object_1=objects_table[object_1],
            object_2=objects_table[object_2],
            relation=objects_table[relation],
        )
        for object_1, relation, object_2 in semantic_network.values()
    ]

    instances_text = "\n".join(list_instances)
    return f"""{instances_text}

hermano(X, Y) :-
    padre(Z, X),
    padre(Z, Y),
    madre(W, X),
    madre(W, Y),
    X \= Y.

tio(X, Y) :-
    hermano(X, Z),
    (padre(Z, Y); madre(Z, Y)).

abuelo(X,Y):-
    madre(X, Z),
    madre(Z, Y);
    madre(X, Z),
    padre(Z, Y);
    padre(X, Z),
    madre(Z, Y);
    padre(X, Z),
    padre(Z, Y).

primo(X, Y) :-
    abuelo(Z, X),
    abuelo(Z, Y),
    X \= Y,
    not(hermano(X, Y))."""

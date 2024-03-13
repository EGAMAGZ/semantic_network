from abc import ABC, abstractmethod
import re
from typing import Literal, override

from util.mermaid import ObjectsTable, SemanticNetwork, generate_mermaid
from util.text import TextInfo, divide_text, to_prolog_instance


class AbtractGenerator(ABC):
    _generated_code: str
    _semantic_network: SemanticNetwork
    _objects_table: ObjectsTable
    _mermaid_code: str

    @abstractmethod
    def generate(self) -> None: ...

    @property
    def generated_code(self) -> str:
        return self._generated_code

    @generated_code.setter
    def generated_code(self, code: str) -> None:
        self._generated_code = code

    @property
    def mermaid_code(self) -> str:
        return self._mermaid_code

    @mermaid_code.setter
    def mermaid_code(self, code: str) -> None:
        self._mermaid_code = code

    @property
    def semantic_network(self) -> SemanticNetwork:
        return self._semantic_network

    @semantic_network.setter
    def semantic_network(self, semantic_network: SemanticNetwork) -> None:
        self._semantic_network = semantic_network

    @property
    def objects_table(self) -> ObjectsTable:
        return self._objects_table

    @objects_table.setter
    def objects_table(self, objects_table: ObjectsTable) -> None:
        self._objects_table = objects_table


class SemanticNetworkGenerator(AbtractGenerator):

    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text

    @override
    def generate(self) -> None:
        sentences: list[str] = self._text.replace("\n", "").split(".")

        objects_table: ObjectsTable = {}
        total_objects: int = 0

        number_row = 0
        semantic_network: SemanticNetwork = {}

        words_index: dict[TextInfo, int] = {}

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

        self.semantic_network = semantic_network
        self.objects_table = objects_table
        self.generated_code = generate_mermaid(objects_table, semantic_network)
        self.mermaid_code = generate_mermaid(objects_table, semantic_network)


class FamilyTreeGenerator(AbtractGenerator):
    _text: str

    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text

    @override
    def generate(self) -> None:
        sentences: list[str] = self._text.replace("\n", "").split(".")

        number_row_table = 0
        number_row_network = 0
        object_table: ObjectsTable = {}
        words_index: dict[str, int] = {}
        semantic_network: SemanticNetwork = {}
        genres_table: dict[Literal["hombre", "mujer"], set[str]] = {
            "hombre": set(),
            "mujer": set(),
        }

        group_1: list[str] = []
        group_2: list[str] = []
        group_3: list[str] = []

        for sentence in sentences:
            if not sentence:
                continue

            is_group_3 = False
            group_1 = []
            group_2 = []
            group_3 = []

            type_sentence: Literal["R", "O"] | None = None
            current_word = ""
            clean_sentence = sentence.strip()

            for character in clean_sentence:
                if character == "(":
                    type_sentence = "O"

                if character == "[":
                    is_group_3 = True
                    type_sentence = "R"

                if type_sentence:
                    current_word += character

                if character == ")" or character == "]":
                    if type_sentence == "R":
                        group_2.append(re.sub(r"[\[\]\(\)]", "", current_word))

                    if type_sentence == "O" and is_group_3:
                        group_3.append(re.sub(r"[\[\]\(\)]", "", current_word))

                    if type_sentence == "O" and not is_group_3:
                        group_1.append(re.sub(r"[\[\]\(\)]", "", current_word))

                    current_object = (
                        re.sub(r"[\[\]\(\)]", "", current_word),
                        type_sentence,
                    )

                    if current_object not in object_table.values():
                        number_row_table += 1
                        object_table[number_row_table] = current_object
                        words_index[re.sub(r"[\[\]\(\)]", "", current_word)] = (
                            number_row_table
                        )

                    type_sentence = None
                    current_word = ""

            for object_1 in group_1:
                for relation in group_2:
                    for object_2 in group_3:
                        number_row_network += 1
                        semantic_network[number_row_network] = (
                            words_index[object_1],
                            words_index[relation],
                            words_index[object_2],
                        )
                        if relation == "es":
                            genres_table[object_2].add(object_1)

        self.semantic_network = semantic_network
        self.objects_table = object_table
        self.mermaid_code = generate_mermaid(object_table, semantic_network)
        self.generated_code = self._generate_prolog_code(
            semantic_network, object_table, genres_table
        )

    def _generate_prolog_code(
        self,
        semantic_network: SemanticNetwork,
        objects_table: ObjectsTable,
        genres_table: dict[str, set[str]],
    ) -> str:
        list_instances = [
            to_prolog_instance(
                object_1=objects_table[object_1],
                object_2=objects_table[object_2],
                relation=objects_table[relation],
            )
            for object_1, relation, object_2 in semantic_network.values()
            if relation == "es"
        ]

        list_instances.extend(
            [
                f"{genre}({name})."
                for genre, names in genres_table.items()
                for name in names
            ]
        )

        instances_text = "\n".join(list_instances)
        return f"""{instances_text}
sibling(X, Y) :-
    padre(Z, X),
    padre(Z, Y),
    madre(W, X),
    madre(W, Y),
    X \= Y.

hermano(X,Y):-
    sibling(X,Y),
    hombre(X).

hermana(X,Y) :-
    sibling(X,Y),
    mujer(X).

gran(X,Y):-
    madre(X, Z),
    madre(Z, Y);

    madre(X, Z),
    padre(Z, Y);

    padre(X, Z),
    madre(Z, Y);

    padre(X, Z),
    padre(Z, Y).

abuelo(X, Y) :-
    gran(X,Y),
    hombre(X).

abuela(X, Y) :-
    gran(X,Y),
    mujer(X).
"""

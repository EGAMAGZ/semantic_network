from abc import ABC, abstractmethod
from typing import override

from util.mermaid import ObjectsTable, SemanticNetwork, generate_mermaid
from util.text import TextInfo, divide_text


class AbtractGenerator(ABC):
    _generated_code: str
    _semantic_network: SemanticNetwork
    _objects_table: ObjectsTable

    @abstractmethod
    def generate(self) -> None: ...

    @property
    def generated_code(self) -> str:
        return self._generated_code

    @generated_code.setter
    def generated_code(self, code: str) -> None:
        self._generated_code = code

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


class FamilyTreeGenerator(AbtractGenerator):
    _text: str

    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text

    @override
    def generate(self) -> None:
        pass

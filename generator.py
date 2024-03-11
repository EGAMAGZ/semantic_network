from abc import ABC, abstractmethod


class AbtractGenerator(ABC):

    @abstractmethod
    def generate(self) -> None: ...

    @property
    @abstractmethod
    def get_generated_code(self) -> str: ...

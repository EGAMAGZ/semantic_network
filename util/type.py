from typing import Literal


type TextInfo = tuple[str, Literal["R", "O"]]

type SemanticNetwork = dict[int, tuple[int, int, int]]

type ObjectsTable = dict[int, TextInfo]
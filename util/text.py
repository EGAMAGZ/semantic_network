import re
from typing import Literal

type TextInfo = tuple[str, Literal["R", "O"]]


def divide_text(sentence: str) -> tuple[list[TextInfo], list[TextInfo], list[TextInfo]]:

    pattern = r"(?P<grupo1>\(.*?\))\s*(?=\[)(?P<grupo2>\[.*?\])\s*(?P<grupo3>\(.*?\))"

    coincidences = re.search(pattern, sentence)

    group_1: list[TextInfo] = list(
        map(
            lambda text: (re.sub(r"[\(\)]", "", text), "O"),
            re.findall(r"\(.*?\)", coincidences.group("grupo1")),
        )
    )
    group_2: list[TextInfo] = list(
        map(
            lambda text: (re.sub(r"[\[\]]", "", text), "R"),
            re.findall(r"\[.*?\]", coincidences.group("grupo2")),
        )
    )
    group_3: list[TextInfo] = list(
        map(
            lambda text: (re.sub(r"[\(\)]", "", text), "O"),
            re.findall(
                r"\(.*?\)",
                coincidences.group("grupo3") + sentence[coincidences.end() :],
            ),
        )
    )

    return (group_1, group_2, group_3)


if __name__ == "__main__":
    text = "(el agua) y (el jabon) [se usan en] y [se encuentran en] (la casa), (la escuela) y (la oficina)."
    groups = divide_text(text)

    assert groups == [
        [("(el agua)", "O"), ("(el jabon)", "O")],
        [("[se usan en]", "R"), ("[se encuentran en]", "R")],
        [("(la casa)", "O"), ("(la escuela)", "O"), ("(la oficina)", "O")],
    ]

    text = "(Gamaliel) [juegan] y [se divierte] (la casa)"
    groups = divide_text(text)

    assert groups == [
        [("(Gamaliel)", "O")],
        [("[juegan]", "R"), ("[se divierte]", "R")],
        [("(la casa)", "O")],
    ]

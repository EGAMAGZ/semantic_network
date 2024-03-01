def main() -> None:
    with open("entrada.txt") as file:
        text = file.read().replace("\n", "")
    sentences = text.split(".")

    lexico: dict[str, tuple[str, str]] = {}

    object_count = 0
    relation_count = 0
    for sentence in sentences:
        print("<start>")
        clean_sentence = sentence.strip()
        in_object = False
        in_relation = False

        current_object = ""
        current_relation = ""

        for char in clean_sentence:
            if char == "(":
                in_object = True
                object_count += 1
                current_object = ""

            if in_object:
                current_object += char

            if char == ")":
                lexico[str(object_count)] = (current_object, "O")
                print(f"Object #{object_count}: {current_object}")

            if char == "[":
                in_relation = True
                relation_count += 1
                current_relation = ""

            if in_relation:
                current_relation += char

            if char == "]":
                lexico[str(relation_count)] = (current_relation, "R")
                print(f"Relation #{relation_count}: {current_relation}")
        print("</start>")

    print(lexico)


if __name__ == "__main__":
    main()

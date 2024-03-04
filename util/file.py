import csv
from util.mermaid import ObjectsTable, SemanticNetwork


def register_semantic_csv(content: SemanticNetwork) -> None:
    with open("data/semantic.csv", "w") as file:
        csv_file = csv.DictWriter(file, ["id", "object_1", "relation", "object_2"])
        csv_file.writeheader()
        for key, (object_1, relation, object_2) in content.items():
            csv_file.writerow(
                {
                    "id": key,
                    "object_1": object_1,
                    "relation": relation,
                    "object_2": object_2,
                }
            )


def register_objects_csv(content: ObjectsTable) -> None:
    with open("data/objects.csv", "w") as file:
        csv_file = csv.DictWriter(file, ["id", "object", "type"])
        csv_file.writeheader()
        for key, (text, object_type) in content.items():
            csv_file.writerow({"id": key, "object": text, "type": object_type})

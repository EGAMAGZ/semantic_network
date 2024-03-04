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


def get_objects_table() -> ObjectsTable:
    objects_table: ObjectsTable = {}
    with open("data/objects.csv") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            objects_table[int(row["id"])] = (row["object"], row["type"])
    return objects_table


def get_semantic_table() -> SemanticNetwork:
    semantic_table: SemanticNetwork = {}
    with open("data/semantic.csv") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            semantic_table[int(row["id"])] = (
                int(row["object_1"]),
                int(row["relation"]),
                int(row["object_2"]),
            )
    return semantic_table

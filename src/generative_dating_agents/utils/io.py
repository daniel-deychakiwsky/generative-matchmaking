import os
from typing import Any, List

import jsonlines


def read_jsonl_file(input_filepath: str) -> List:
    with jsonlines.open(input_filepath, "r") as jsonl_f:
        return list(jsonl_f)


def write_jsonl_file(json_array: List[Any], output_filepath: str) -> None:
    if os.path.exists(output_filepath):
        with jsonlines.open(output_filepath, "a") as writer:
            writer.write_all(json_array)
    else:
        with jsonlines.open(output_filepath, "w") as writer:
            writer.write_all(json_array)

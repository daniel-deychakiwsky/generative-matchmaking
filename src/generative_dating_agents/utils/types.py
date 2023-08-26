from typing import Dict, List, Union

JSON = Dict[
    str,
    Union[
        str,
        int,
        float,
        bool,
        None,
        "JSON",
        List[Union[str, int, float, bool, None, "JSON"]],
    ],
]

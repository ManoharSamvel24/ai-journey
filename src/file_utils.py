from typing import Iterator


def read_lines_lazy(path: str) -> Iterator[str]:
    with open(path, "r") as f:
        for line in f:
            yield line.strip()
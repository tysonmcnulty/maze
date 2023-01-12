from pathlib import Path


def load(data_file: Path) -> list[str]:
    with open(data_file) as data:
        return [*data]


def parse(data: list[str]):
    pass

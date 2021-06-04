import pathlib


def read_fixture(filename: str) -> str:
    path = pathlib.Path(__file__).parent / f"./fixtures/{filename}"
    with open(path) as f:
        return f.read()

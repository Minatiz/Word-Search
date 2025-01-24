def read_word(file_path) -> set:
    with open(file_path, "r") as f:
        return set(line.strip() for line in f.readlines())


def read_grid(file_path) -> str:
    with open(file_path, "r") as f:
        return f.read()
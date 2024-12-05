import glob


def get_docs() -> list[str]:
    docs = []
    for path in glob.glob("data/*.txt"):
        with open(path, 'r') as file:
            docs.append(file.read())
    return docs


def tokenize(text):
    return text.lower().split(" ")

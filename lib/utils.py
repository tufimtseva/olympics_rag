import glob


def get_docs() -> list[str]:
    chunks = []
    current_chunk = []
    path = glob.glob("olympic_games_chunks.txt")
    print(path)

    with open(path[0], "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Chunk") and line.endswith(":"):
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
            else:
                current_chunk.append(line)
        if current_chunk:
            chunks.append(" ".join(current_chunk))

    print(f"Total chunks read: {len(chunks)}")
    return chunks[:50]



def tokenize(text):
    return text.lower().split(" ")

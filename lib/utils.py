import glob

CONTEXT_PREFIX_LEN = 30

def get_docs_and_headers() -> tuple[list[str], dict[str, str]]:
    """
    Reads chunks and their headers from a text file and returns a list of chunks
    and a dictionary mapping each chunk to its header.

    Returns:
        tuple: A tuple containing:
            - list of chunks (list[str])
            - map of chunk to header (dict[str, str])
    """
    chunks = []
    chunk_header_map = {}
    current_chunk = []
    current_header = ""

    paths = glob.glob("olympic_games_chunks.txt")
    if not paths:
        raise FileNotFoundError("No file matching the pattern 'olympic_games_chunks.txt' found.")
    file_path = paths[0]

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Chunk") and line.endswith(":"):
                if current_chunk:
                    chunk_text = " ".join(current_chunk)
                    chunks.append(chunk_text)
                    chunk_header_map[chunk_text[:CONTEXT_PREFIX_LEN]] = current_header
                    current_chunk = []
                current_header = ""
            elif line.startswith("Header:"):
                current_header = line.split("Header:", 1)[1].strip()
            else:
                current_chunk.append(line)

        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)
            chunk_header_map[chunk_text[:CONTEXT_PREFIX_LEN]] = current_header

    print(f"Total chunks read: {len(chunks)}")
    return chunks, chunk_header_map


def tokenize(text):
    return text.lower().split(" ")

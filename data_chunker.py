from nltk import sent_tokenize
from sentence_transformers import SentenceTransformer, util


def read_text_file(file_path):
    """
    Read text from a file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: Text content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def chunk_text_by_themes(text, similarity_threshold=0.5):
    """
    Chunk text into thematic groups based on semantic similarity.

    Args:
        text (str): Input text to be chunked.
        similarity_threshold (float): Minimum similarity score for grouping sentences.

    Returns:
        list: List of thematic chunks.
    """
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    sentences = sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = util.cos_sim(embeddings[i - 1], embeddings[i]).item()
        # print(similarity)
        if similarity > similarity_threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def save_chunks_to_file(chunks, file_path):
    """
    Save semantic chunks to a file.

    Args:
        chunks (list): List of text chunks.
        file_path (str): Path to save the chunks.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        for i, chunk in enumerate(chunks, 1):
            file.write(f"Chunk {i}:\n{chunk}\n\n")


if __name__ == "__main__":
    input_file = "olympic_games_plain_text.txt"
    output_file = "olympic_games_chunks.txt"

    full_text = read_text_file(input_file)
    thematic_chunks = chunk_text_by_themes(full_text, similarity_threshold=0.3)
    save_chunks_to_file(thematic_chunks, output_file)

    print(f"Thematic chunks saved to {output_file}.")

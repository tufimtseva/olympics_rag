import re
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


def chunk_text_by_themes(text, headings, similarity_threshold=0.5):
    """
    Chunk text into thematic groups based on semantic similarity.

    Args:
        text (str): Input text to be chunked.
        headings: (list): List of headers.
        similarity_threshold (float): Minimum similarity score for grouping sentences.

    Returns:
        list: List of thematic chunks.
    """
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    sentences = sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)

    chunks = []
    headers = []
    current_chunk = [sentences[0]]
    current_header_idx = 0

    for i in range(1, len(sentences)):
        # print("Heading:", headings[current_header_idx + 1].replace("_", " "),
        #       "\nSentence:", sentences[i],
        #       "\n")
        if_max_min_header = False
        while not if_max_min_header:
            if current_header_idx + 1 < len(headings):
                if headings[current_header_idx + 1].replace("_", " ") in sentences[i]:
                    if current_header_idx + 1 < len(headings):
                        current_header_idx += 1
                    else:
                        if_max_min_header = True
                else:
                    if_max_min_header = True
            else:
                break
        similarity = util.cos_sim(embeddings[i - 1], embeddings[i]).item()
        # print(similarity)
        if similarity > similarity_threshold:
            current_chunk.append(sentences[i])
        else:
            headers.append(headings[current_header_idx])
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    if current_chunk:
        chunks.append(" ".join(current_chunk))
        headers.append(headings[current_header_idx])

    return chunks, headers


def save_chunks_to_file(chunks, headers, file_path):
    """
    Save semantic chunks to a file.

    Args:
        chunks (list): List of text chunks.
        headers: (list): List of headers.
        file_path (str): Path to save the chunks.
    """

    if len(chunks) != len(headers):
        raise ValueError("The number of chunks and headers must be the same.")

    with open(file_path, "w", encoding="utf-8") as file:
        for i, (chunk, header) in enumerate(zip(chunks, headers), start=1):
            file.write(f"Chunk {i}:\n")
            file.write(f"Header: {header}\n")
            file.write(f"{chunk}\n")
            file.write("\n")


def extract_headings(text):
    """
    Extract headings or subtopics from plain text.

    Args:
        text (str): Input text containing potential headings.

    Returns:
        list: A list of extracted headings/subtopics.
    """
    pattern = r"^(?:\s*)[A-Z][a-zA-Z0-9\s,']+?(?=\n)"
    matches = re.findall(pattern, text, re.MULTILINE)
    headings = [heading.strip().replace(" ", "_") for heading in matches if len(heading.strip()) > 3]

    return headings


if __name__ == "__main__":
    input_file = "olympic_games_plain_text.txt"
    output_file = "olympic_games_chunks.txt"

    full_text = read_text_file(input_file)
    text_headings = extract_headings(full_text)

    thematic_chunks, text_headers = chunk_text_by_themes(full_text, [""] + text_headings, similarity_threshold=0.3)
    save_chunks_to_file(thematic_chunks, text_headers, output_file)

    print(f"Thematic chunks saved to {output_file}.")

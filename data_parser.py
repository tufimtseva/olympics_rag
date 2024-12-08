import wikipediaapi


def get_wikipedia_page_text(page_title, lang="en"):
    """
    Fetch the text content of a Wikipedia page.

    Args:
        page_title (str): Title of the Wikipedia page.
        lang (str): Language code (default is 'en' for English).

    Returns:
        str: Text content of the page or an error message.
    """
    user_agent = "khrystyna.dol@gmail.com"
    wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=lang)
    page = wiki.page(page_title)

    if not page.exists():
        return f"The page '{page_title}' does not exist in {lang} Wikipedia."

    return page.text


def save_text_to_file(text, file_path):
    """
    Save text content to a .txt file.

    Args:
        text (str): The text to save.
        file_path (str): Path to the file where text will be saved.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


if __name__ == "__main__":
    title = "Olympic Games"
    path = "olympic_games_plain_text.txt"

    page_text = get_wikipedia_page_text(title)
    save_text_to_file(page_text, path)
    # print(page_text[:500])

import os
import streamlit as st
from streamlit_chat import message
from lib.utils import get_docs
from groq_llm import LLM

os.environ['GROQ_API_KEY'] = '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'
def build_chat_ui(docs: list[str]):
    params = {
        "BM25": False
    }
    bm_25_search = st.checkbox("Search by keyword")
    if bm_25_search:
        params["BM25"] = True
    print("params now ", params)

    if "messages" not in st.session_state:
        greeting = "Hi there :)"
        st.session_state.messages = [{"role": "assistant", "content": greeting}]

    for i, m in enumerate(st.session_state.messages):
        if m["role"] == "user":
            message(m["content"], is_user=True, key=f"user_{i}")
        else:
            message(m["content"], key=f"assistant_{i}")

    llm = LLM(docs, params)
    query = st.chat_input("Say something")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        message(query, is_user=True,
                key=f"user_input_{len(st.session_state.messages)}")

        answer = llm.answer_question(query)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer})
        message(answer,
                key=f"assistant_response_{len(st.session_state.messages)}")


if __name__ == "__main__":
    docs = get_docs()
    build_chat_ui(docs)

# to run with web ui: streamlit run /Users/tanya/nlp/main.py

# intro
# Over 14,000 athletes competed at the 2020 Summer Olympics and 2022 Winter Olympics combined, in 40 different sports and 448 events.
# How many sportsmen participated at the 2020 Summer Olympics and 2022 Winter Olympics?

# host nations
# By 2032, the Olympic Games will have been hosted by 47 cities in 23 countries
# How many countries will host Olympics by 2032?

# medalists
# The current three-medal format was introduced at the 1904 Olympics.
# When was the current three-medal format introduced ?

# tell me the most interesting fact about Olympics?

import os
import streamlit as st
from streamlit_chat import message
from lib.utils import get_docs_and_headers
from groq_llm import LLM

def build_chat_ui(docs: list[str], chunk_header_map: dict[str, str]):
    params = {
        "BM25_retriever": False,
        "sBERT_retriever": False
    }
    with st.sidebar:
        option = st.selectbox("Search type", ("None", "By keyword", "Semantic"))
        llm_key = st.text_input(
            "Enter your LLM key for groq model 👇",
        )

        if llm_key:
            st.write("Your LLM key: ", llm_key)
            os.environ['GROQ_API_KEY'] = llm_key

    print("Search option:", option)
    if option == "By keyword":
        params["BM25_retriever"] = True
    elif option == "Semantic":
        params["sBERT_retriever"] = True
    print("params now ", params)

    if "messages" not in st.session_state:
        greeting = "Hi there :)"
        st.session_state.messages = [{"role": "assistant", "content": greeting}]

    for i, m in enumerate(st.session_state.messages):
        if m["role"] == "user":
            message(m["content"], is_user=True, key=f"user_{i}")
        else:
            message(m["content"], key=f"assistant_{i}")
            if "sources" in m:
                st.markdown("### Sources:")
                cols = st.columns(len(m["sources"]))
                for idx, cont_i in enumerate(m["sources"]):
                    with cols[idx]:
                        st.caption(f"Closest subtopic:\n {cont_i['closest_subtopic']}"
                                   f"\nContent:\n {cont_i['content_snippet']}...")
                        st.markdown(f"Link: {cont_i['link']}")

    llm = LLM(docs, chunk_header_map, params)
    query = st.chat_input("Say something")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        message(query, is_user=True,
                key=f"user_input_{len(st.session_state.messages)}")

        answer, context, headers = llm.answer_question(query)

        message(answer, key=f"assistant_response_{len(st.session_state.messages)}")
        if params["BM25_retriever"] or params["sBERT_retriever"]:
            st.markdown("### Sources:")
            cols = st.columns(len(context))

            sources = []
            for i, source in enumerate(context):
                with cols[i]:
                    st.caption(f"Closest subtopic:\n {headers[i].replace('_', ' ')}"
                               f"\nContent:\n {source[:20].replace('**', '')}...")
                    st.markdown(f"Link: https://en.wikipedia.org/wiki/Olympic_Games#{headers[i]}")
                    sources.append({
                        "closest_subtopic": headers[i].replace('_', ' '),
                        "content_snippet": source[:20].replace("**", ""),
                        "link": f"https://en.wikipedia.org/wiki/Olympic_Games#{headers[i]}"
                    })

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })


if __name__ == "__main__":
    all_docs, all_chunk_header_map = get_docs_and_headers()
    build_chat_ui(all_docs, all_chunk_header_map)

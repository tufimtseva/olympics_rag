import os
from litellm import completion
import streamlit as st
from streamlit_chat import message

os.environ['GROQ_API_KEY'] = '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'


class LLM:
    def answer_question(self, question):
        response = completion(
            model="groq/llama3-8b-8192",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that can answer questions. If you don not know the answer say that you do not know it."},
                {"role": "user", "content": question}
            ],
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    message("Hi there :)")
    llm = LLM()
    question = st.chat_input("Say something")
    if question:
        message(question, is_user=True)
        answer = llm.answer_question(question)
        message(answer)

# to run with web ui: streamlit run /Users/tanya/nlp/main.py
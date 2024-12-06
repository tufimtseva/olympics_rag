from litellm import completion
from retriever import Retriever
from bert_retriever import BertRetriever


class LLM:
    PROMPT = "You are a helpful assistant that can answer questions. " \
             "If you don not know the answer say that you do not know it." \
             "Use the provided context to answer questions."

    def __init__(self, docs: list[str], params: dict[str, bool]):
        self.docs = docs
        self.retriever = Retriever(docs)
        self.bert_retriever = BertRetriever(docs)
        self.params = params

    def answer_question(self, query):
        if self.params["BM25_retriever"]:
            context = self.retriever.get_relevant_docs(query)
        elif self.params["sBERT_retriever"]:
            context = self.bert_retriever.get_relevant_docs(query)
        else:
            context = self.docs[:50]
        response = completion(
            model="groq/llama3-8b-8192",
            messages=[
                {"role": "system", "content": self.PROMPT},
                {"role": "user",
                 "content": f"Context: {context} \n Query: {query}"}
            ],
        )
        return response.choices[0].message.content

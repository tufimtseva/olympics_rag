from litellm import completion
from retriever import Retriever
from rerankers import Reranker

class LLM:
    PROMPT = "You are a helpful assistant that can answer questions. " \
             "If you don not know the answer say that you do not know it." \
             "Use the provided context to answer questions."

    def __init__(self, docs: list[str], params: dict[str, bool]):
        self.docs = docs
        self.retriever = Retriever(docs)
        self.params = params

    def answer_question(self, query):
        context = self.retriever.get_relevant_docs(query) if self.params[
            "BM25"] else self.docs[:50]
        if self.params["BM25"] or self.params["dense_retriever"]:
            reranker = Reranker('cross-encoder', model_type='cross-encoder')
            sorted_context = reranker.rank(query, context)
            context = [r.document.text for r in sorted_context.top_k(3)]
        response = completion(
            model="groq/llama3-8b-8192",
            messages=[
                {"role": "system", "content": self.PROMPT},
                {"role": "user",
                 "content": f"Context: {context} \n Query: {query}"}
            ],
        )
        return response.choices[0].message.content

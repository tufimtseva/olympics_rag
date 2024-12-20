from litellm import completion

from lib.utils import CONTEXT_PREFIX_LEN
from retriever import Retriever
from bert_retriever import BertRetriever
from rerankers import Reranker

MAX_CONTEXT_LEN = 50

class LLM:
    PROMPT = "You are a helpful assistant that can answer questions. " \
             "If you don not know the answer say that you do not know it." \
             "Use the provided context to answer questions."

    def __init__(self, docs: list[str], docs_headers_map: dict[str, str], params: dict[str, bool]):
        self.docs = docs
        self.docs_headers_map = docs_headers_map
        self.bm25_retriever = Retriever(docs)
        self.bert_retriever = BertRetriever(docs)
        self.params = params

    def answer_question(self, query):
        if self.params["BM25_retriever"]:
            context = self.bm25_retriever.get_relevant_docs(query)
            print("Retrieved documents after applying keyword search:\n")
            for idx, doc in enumerate(context, 1):
                print(f"Document {idx}:")
                print(doc)
                print("-" * 80)
        elif self.params["sBERT_retriever"]:
            context = self.bert_retriever.get_relevant_docs(query)
            print("Retrieved documents after applying semantic search:\n")
            for idx, doc in enumerate(context, 1):
                print(f"Document {idx}:")
                print(doc)
                print("-" * 80)
        else:
            context = self.docs[:MAX_CONTEXT_LEN]
        if self.params["BM25_retriever"] or self.params["sBERT_retriever"]:
            reranker = Reranker('cross-encoder', model_type='cross-encoder')
            sorted_context = reranker.rank(query, context)
            print("Reranked documents after applying cross-encoder model:\n")
            for idx, doc in enumerate(sorted_context, 1):
                print(f"Document {idx}:")
                print(doc)
                print("-" * 80)
            context = [r.document.text for r in sorted_context.top_k(3)]

        headers = [self.docs_headers_map[c[:CONTEXT_PREFIX_LEN]] for c in context]
        response = completion(
            model="groq/llama3-8b-8192",
            messages=[
                {"role": "system", "content": self.PROMPT},
                {"role": "user",
                 "content": f"Context: {context} \n Query: {query}"}
            ],
        )
        return response.choices[0].message.content, context[:3], headers

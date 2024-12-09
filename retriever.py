from rank_bm25 import BM25Okapi
import numpy as np
from lib.utils import tokenize


class Retriever:
    def __init__(self, docs: list[str]):
        self.docs = docs
        tokenized_docs = [tokenize(doc) for doc in self.docs]
        self.bm25 = BM25Okapi(tokenized_docs)

    def get_relevant_docs(self, query: str, n=10) -> list[str]:
        tokenized_query = tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_n = np.argsort(scores)[::-1][:n]
        return [self.docs[i] for i in top_n]

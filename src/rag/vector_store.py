"""Regulatory retrieval backend; TF-IDF default, FAISS optional."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
class RegulatoryStore:
    def __init__(self,chunks,backend='tfidf',model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.chunks=chunks;self.backend=backend
        if not chunks:return
        texts=[c['text'] for c in chunks]
        if backend=='semantic':
            from src.retrieval.embeddings import Embeddings
            from src.retrieval.faiss_index import create_index
            self.encoder=Embeddings(model_name);self.index=create_index(self.encoder.encode(texts))
        else:
            self.vectorizer=TfidfVectorizer(ngram_range=(1,2));self.matrix=self.vectorizer.fit_transform(texts)
    def search(self,query,k=4):
        if not self.chunks:return []
        if self.backend=='semantic':
            scores,indices=self.index.search(self.encoder.encode([query]),min(k,len(self.chunks)));pairs=zip(indices[0],scores[0])
        else:
            scores=cosine_similarity(self.vectorizer.transform([query]),self.matrix).ravel();pairs=[(i,scores[i]) for i in np.argsort(-scores)[:k]]
        return [{**self.chunks[int(i)],'retrieval_score':round(float(s),4)} for i,s in pairs if i>=0 and s>0]

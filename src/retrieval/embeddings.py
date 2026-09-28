"""Sentence Transformer adapter. Model installation is explicit."""
import numpy as np
class Embeddings:
    def __init__(self,model_name):
        from sentence_transformers import SentenceTransformer
        self.model=SentenceTransformer(model_name)
    def encode(self,texts):
        return np.asarray(self.model.encode(list(texts),normalize_embeddings=True,show_progress_bar=False),dtype='float32')

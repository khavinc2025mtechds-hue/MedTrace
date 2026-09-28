"""Normalized inner-product FAISS search (cosine similarity, not probability)."""
import numpy as np

def create_index(vectors):
    import faiss
    vectors=np.ascontiguousarray(vectors,dtype='float32');index=faiss.IndexFlatIP(vectors.shape[1]);index.add(vectors);return index

def save_index(index,filename):
    import faiss
    faiss.write_index(index,str(filename))

def read_index(filename):
    import faiss
    return faiss.read_index(str(filename))

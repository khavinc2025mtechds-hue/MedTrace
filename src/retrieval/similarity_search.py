"""Case retrieval with TF-IDF baseline and explicit semantic backend."""
import argparse
import hashlib
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config.settings import path,settings
from src.ingestion.load_maude import load

class CaseSearch:
    def __init__(self,frame=None,backend=None):
        cfg=settings();self.cfg=cfg['retrieval'];self.backend=backend or self.cfg['backend']
        if frame is None:
            f=path(cfg['data']['processed']);f=f if f.exists() else path(cfg['data']['sample'])
            frame=load(str(f)) if f.exists() else pd.DataFrame()
        self.frame=frame.fillna('').drop_duplicates('mdr_report_key').reset_index(drop=True) if len(frame) else frame
        self.vectorizer=None;self.matrix=None
        if self.frame.empty:return
        texts=self.frame.narrative.astype(str).tolist()
        if self.backend=='semantic':
            from src.retrieval.embeddings import Embeddings
            from src.retrieval.faiss_index import create_index
            self.encoder=Embeddings(self.cfg['embedding_model']);self.matrix=self.encoder.encode(texts);self.index=create_index(self.matrix)
        elif self.backend=='tfidf':
            self.vectorizer=TfidfVectorizer(ngram_range=(1,2),max_features=50000,sublinear_tf=True)
            self.matrix=self.vectorizer.fit_transform(texts)
        else:raise ValueError('retrieval backend must be tfidf or semantic')

    def search(self,query,top_k=None,exclude_ids=None,as_of=None):
        if self.frame.empty:return []
        top_k=top_k or self.cfg['top_k'];exclude=set(map(str,exclude_ids or []))
        if self.backend=='semantic':
            scores,indices=self.index.search(self.encoder.encode([query]),len(self.frame));pairs=zip(indices[0],scores[0])
        else:
            scores=cosine_similarity(self.vectorizer.transform([query]),self.matrix).ravel();pairs=((i,scores[i]) for i in np.argsort(-scores,kind='stable'))
        rows=[];hashes=set();query_norm=' '.join(query.casefold().split())
        cutoff=pd.Timestamp(as_of) if as_of else None
        for idx,score in pairs:
            row=self.frame.iloc[int(idx)].to_dict()
            if str(row['mdr_report_key']) in exclude or score<self.cfg['min_score']:continue
            if cutoff is not None:
                dt=pd.to_datetime(row.get('date_received'),errors='coerce')
                if pd.isna(dt) or dt>cutoff:continue
            norm=' '.join(row['narrative'].casefold().split())
            if norm==query_norm:continue # held-out complaint cannot retrieve an identical narrative
            h=hashlib.sha256(norm.encode()).hexdigest()
            if h in hashes:continue
            hashes.add(h);row['similarity_score']=round(float(score),4);row['similarity_method']=self.backend;rows.append(row)
            if len(rows)>=top_k:break
        return rows

    def save_semantic(self):
        if self.backend!='semantic':raise ValueError('Build with --backend semantic to save a FAISS index')
        if self.frame.empty:raise ValueError('No data loaded')
        from src.retrieval.faiss_index import save_index
        d=path(self.cfg['index_dir']);d.mkdir(parents=True,exist_ok=True);save_index(self.index,d/'cases.faiss')
        self.frame.to_json(d/'records.json',orient='records',indent=2)
        (d/'metadata.json').write_text(json.dumps({'model':self.cfg['embedding_model'],'rows':len(self.frame),'normalized':True},indent=2))
        return d
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--backend',choices=['tfidf','semantic'],default='semantic');a=p.parse_args();s=CaseSearch(backend=a.backend)
    print(s.save_semantic() if a.backend=='semantic' else f'TF-IDF index ready: {len(s.frame)} reports')

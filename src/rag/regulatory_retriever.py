"""Build a source-indexed corpus and filter evidence by analysis date."""
import argparse
import json
from datetime import date
from config.settings import path,settings
from src.rag.document_loader import load_document
from src.rag.chunker import chunk_documents
from src.rag.vector_store import RegulatoryStore

def build_corpus():
    manifest=path('regulatory_docs/source_manifest.json')
    sources=json.loads(manifest.read_text(encoding='utf-8'));docs=[]
    for source in sources:
        f=path(source['file'])
        if f.exists():docs.extend(load_document(f,source['source_url'],source.get('effective_from',''),source.get('effective_to',''),source.get('retrieved_at','')))
    chunks=chunk_documents(docs);out=path(settings()['regulatory']['corpus']);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(chunks,indent=2),encoding='utf-8');return chunks

def retrieve(query,k=None,as_of=None,backend='tfidf'):
    corpus=path(settings()['regulatory']['corpus'])
    if not corpus.exists():return {'status':'unavailable','analysis_date':as_of or date.today().isoformat(),'evidence':[],'message':'Regulatory corpus not built.'}
    when=as_of or date.today().isoformat();chunks=json.loads(corpus.read_text(encoding='utf-8'))
    # Snapshot applicability is explicit. Historical cases need a historical corpus.
    chunks=[c for c in chunks if (not c.get('effective_from') or c['effective_from']<=when) and (not c.get('effective_to') or when<=c['effective_to'])]
    evidence=RegulatoryStore(chunks,backend,settings()['retrieval']['embedding_model']).search(query,k or settings()['regulatory']['top_k'])
    return {'status':'retrieved' if evidence else 'no_applicable_evidence','analysis_date':when,'evidence':evidence,'message':'Retrieved passages require professional interpretation.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--query');a=p.parse_args()
    print(f'{len(build_corpus())} chunks built' if a.build else json.dumps(retrieve(a.query or 'manufacturer medical device complaint reporting malfunction'),indent=2))

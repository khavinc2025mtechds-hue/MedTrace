"""Overlapping word chunks preserve source section, dates and file hash."""
import hashlib

def chunk_documents(documents,size=220,overlap=40):
    if size<=overlap or overlap<0:raise ValueError('Require size > overlap >= 0')
    chunks=[]
    for doc in documents:
        words=doc['text'].split()
        for start in range(0,len(words),size-overlap):
            text=' '.join(words[start:start+size])
            if not text:continue
            record={**doc,'text':text,'word_start':start}
            record['id']='REG-'+hashlib.sha256((doc['document']+doc['section']+str(start)+text).encode()).hexdigest()[:12]
            chunks.append(record)
            if start+size>=len(words):break
    return chunks

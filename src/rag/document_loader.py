"""Load local PDF/text or eCFR HTML; retain per-section/page provenance."""
import hashlib
from pathlib import Path

def load_document(filename,source_url='',effective_from='',effective_to='',retrieved_at=''):
    p=Path(filename);records=[]
    if p.suffix.lower()=='.pdf':
        from pypdf import PdfReader
        pieces=[(f'page {i+1}',page.extract_text() or '') for i,page in enumerate(PdfReader(p).pages)]
    elif p.suffix.lower() in {'.html','.htm'}:
        from bs4 import BeautifulSoup
        soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        nodes=soup.select('div.section')
        if not nodes:raise ValueError('No eCFR section elements found. Export selected official text as .txt with provenance.')
        pieces=[]
        for n in nodes:
            for x in n.select('.section-tools, .paragraph-tools, script, style'):x.decompose()
            pieces.append((n.get('id','section'),n.get_text(' ',strip=True)))
    else:pieces=[(p.stem,p.read_text(encoding='utf-8'))]
    for section,text in pieces:
        text=' '.join(text.split())
        if not text:continue
        records.append({'text':text,'section':section,'source_url':source_url,'document':p.name,'effective_from':effective_from,'effective_to':effective_to,'retrieved_at':retrieved_at,'document_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return records

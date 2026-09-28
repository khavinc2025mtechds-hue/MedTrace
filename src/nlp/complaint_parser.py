"""Parse complaint and report missing identity and outcome information."""
from src.nlp.entity_extractor import extract

def parse_complaint(text: str, fields=None):
    if not text or len(text.strip())<10:raise ValueError('Enter at least 10 characters of complaint text')
    result=extract(text,fields,use_spacy=True)
    result['missing_evidence']=[label for key,label in [('manufacturer','Manufacturer'),('model','Device model')] if not result[key]]
    if result['patient_impact']=='Not reported':result['missing_evidence'].append('Patient outcome')
    from src.nlp.classifier_inference import predict
    result['classification']=predict(text)
    return result

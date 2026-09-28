"""Optional trained classification; keep predictions separate from extracted facts."""
import os
from functools import lru_cache
from config.settings import path
@lru_cache(maxsize=2)
def load_model(backend):
    if backend=='baseline':
        import joblib
        p=path('models/classifiers/baseline.joblib')
        if not p.exists():raise FileNotFoundError('Train baseline_classifier on reviewed labels first')
        return joblib.load(p)
    if backend=='transformer':
        from transformers import pipeline
        p=path('models/classifiers/transformer')
        if not (p/'config.json').exists():raise FileNotFoundError('Train bert_classifier on reviewed labels first')
        return pipeline('text-classification',model=str(p),tokenizer=str(p),device=-1)
    raise ValueError('CLASSIFIER_BACKEND must be rules, baseline or transformer')
def predict(text):
    backend=os.getenv('CLASSIFIER_BACKEND','rules')
    if backend=='rules':return {'status':'disabled','backend':'rules','note':'No trained classifier active; evidence extraction uses rules.'}
    model=load_model(backend)
    if backend=='baseline':
        probabilities=model.predict_proba([text])[0];i=int(probabilities.argmax());label=str(model.classes_[i]);score=float(probabilities[i])
    else:
        item=model(text,truncation=True,max_length=256)[0];label=item['label'];score=float(item['score'])
    return {'status':'predicted','backend':backend,'label':label,'model_score':score,'note':'Model score is not calibrated clinical risk. Prediction is not a verified fact.'}

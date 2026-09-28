"""SHAP only explains an actually trained priority model."""
import joblib
from config.settings import path
from src.analytics.priority_model import FEATURES

def explain(features):
    import pandas as pd
    p=path('models/priority/priority.joblib')
    if not p.exists():return {'status':'not_trained','message':'Rule contributions are available. SHAP requires an independently trained priority model.'}
    import shap
    model=joblib.load(p);frame=pd.DataFrame([{k:features.get(k,0) for k in FEATURES}]);result=shap.TreeExplainer(model)(frame)
    return {'status':'available','raw_prediction':float(model.predict(frame)[0]),'base_value':float(result.base_values[0]),'features':[{'name':k,'value':float(frame.iloc[0][k]),'shap_value':float(result.values[0][i])} for i,k in enumerate(FEATURES)],'target':'reviewer priority; no probability interpretation'}

"""Train and evaluate TF-IDF + logistic regression on curated labels."""
import argparse,json,joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix
from config.settings import path
from src.evaluation.splits import labeled_split

def train(csv_path,cutoff=None):
    tr,te=labeled_split(csv_path,cutoff)
    model=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),max_features=50000)),('classifier',LogisticRegression(max_iter=1000,class_weight='balanced',random_state=42))]);model.fit(tr.narrative,tr.label);pred=model.predict(te.narrative)
    out=path('models/classifiers');out.mkdir(parents=True,exist_ok=True);joblib.dump(model,out/'baseline.joblib')
    metrics=classification_report(te.label,pred,output_dict=True,zero_division=0);metrics['confusion_matrix']=confusion_matrix(te.label,pred,labels=model.classes_).tolist();metrics['labels']=model.classes_.tolist();metrics['split']='temporal' if cutoff else 'duplicate-group holdout';metrics['train_rows']=len(tr);metrics['test_rows']=len(te)
    dest=path('reports/evaluation/baseline_metrics.json');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(metrics,indent=2));return metrics
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--cutoff');a=p.parse_args();print(json.dumps(train(a.csv,a.cutoff),indent=2))

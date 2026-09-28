"""Optional XGBoost regression on independently reviewed priority scores."""
import argparse,json,joblib
import pandas as pd
from config.settings import path
FEATURES=['serious_outcome','delivery_interruption','qualified_similar_reports','verified_recall']
def train(csv_path):
    from xgboost import XGBRegressor
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.metrics import mean_absolute_error
    df=pd.read_csv(csv_path)
    required=FEATURES+['reviewer_priority','label_source','case_group']
    if not set(required).issubset(df):raise ValueError('Required columns: '+', '.join(required))
    if len(df)<30 or not df.label_source.eq('human_review').all():raise ValueError('Need 30+ independently human-reviewed rows. Do not train/evaluate against rule-generated targets.')
    if not df.reviewer_priority.between(0,100).all():raise ValueError('Reviewer priority must be 0..100')
    tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(df,groups=df.case_group))
    model=XGBRegressor(n_estimators=100,max_depth=3,learning_rate=.05,random_state=42,n_jobs=2)
    model.fit(df.iloc[tr][FEATURES],df.iloc[tr].reviewer_priority);pred=model.predict(df.iloc[te][FEATURES]).clip(0,100)
    dest=path('models/priority');dest.mkdir(parents=True,exist_ok=True);joblib.dump(model,dest/'priority.joblib')
    metrics={'mae':mean_absolute_error(df.iloc[te].reviewer_priority,pred),'train_rows':len(tr),'test_rows':len(te),'target':'reviewer-assigned priority, not clinical risk'}
    path('reports/evaluation/priority_metrics.json').write_text(json.dumps(metrics,indent=2));return metrics
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');a=p.parse_args();print(train(a.csv))

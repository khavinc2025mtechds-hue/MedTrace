"""Save development-sample EDA figures and missingness summary."""
import json
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from config.settings import path
from src.retrieval.similarity_search import CaseSearch
from src.nlp.entity_extractor import extract
from src.analytics.trend_analysis import analyze_trends

def run():
    df=CaseSearch().frame
    if df.empty:raise ValueError('Load records first')
    out=path('reports/figures');out.mkdir(parents=True,exist_ok=True)
    series={'year':df.date_received.str[:4].value_counts().sort_index(),'event_type':df.event_type.value_counts(),'manufacturer':df.manufacturer.value_counts().head(10),'patient_outcome':df.patient_problems.replace('','Not reported').value_counts().head(10),'problem':df.narrative.map(lambda t:extract(t)['problems'][0]).value_counts()}
    for name,s in series.items():
        fig,ax=plt.subplots(figsize=(11,6));s.index=[textwrap.fill(str(x),45) for x in s.index];s.sort_values().plot.barh(ax=ax,color='#167d9a');ax.set_title('Loaded corpus: '+name+' (report counts)');ax.set_xlabel('Reports');fig.tight_layout();fig.savefig(out/(name+'.png'),bbox_inches='tight');plt.close(fig)
    vec=CountVectorizer(stop_words='english',max_features=30);x=vec.fit_transform(df.narrative)
    terms=sorted(zip(vec.get_feature_names_out(),x.sum(axis=0).A1.tolist()),key=lambda z:-z[1]);path('reports/evaluation/eda.json').write_text(json.dumps({'reports':len(df),'missing':df.eq('').sum().to_dict(),'common_terms':terms,'trends':analyze_trends(df)},indent=2,default=int))
    print('EDA saved to reports/figures and reports/evaluation/eda.json')
if __name__=='__main__':run()

"""Descriptive reporting patterns. Sample counts are never incidence rates."""
import pandas as pd

def analyze_trends(frame,as_of=None,manufacturer='',model=''):
    empty={'monthly':[],'total_reports':0,'scope':'loaded corpus','spike':False,'score_eligible':False,'interpretation':'Insufficient dated records.'}
    if frame.empty:return empty
    df=frame.copy();df['_date']=pd.to_datetime(df.date_received,errors='coerce');df=df.dropna(subset=['_date'])
    if as_of:df=df[df._date<=pd.Timestamp(as_of)]
    if manufacturer:df=df[df.manufacturer.str.casefold().eq(manufacturer.casefold())]
    if model:df=df[df.model.str.casefold().eq(model.casefold())]
    if df.empty:return empty
    series=df.groupby(df._date.dt.to_period('M')).mdr_report_key.nunique()
    series=series.reindex(pd.period_range(series.index.min(),series.index.max(),freq='M'),fill_value=0)
    result={'monthly':[{'month':str(k),'reports':int(v)} for k,v in series.items()], 'total_reports':int(df.mdr_report_key.nunique()),'scope':'matching device identity in loaded corpus' if manufacturer or model else 'all infusion-pump records in loaded corpus','spike':False,'score_eligible':False,'interpretation':'Descriptive report counts only. Incomplete sampling and reporting bias prevent incidence estimates.'}
    # A capped download cannot support an unbiased population trend score.
    if len(series)>=7:
        prior=series.iloc[-7:-1];result['last_month_vs_prior_mean']=round(float(series.iloc[-1]-prior.mean()),2)
        result['spike']=bool(series.iloc[-1]>prior.mean()+3*prior.std(ddof=0) and series.iloc[-1]>=5)
    return result

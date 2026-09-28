"""Explicit code/date filtering. FRN is a starting scope, not all infusion devices."""
import pandas as pd

def filter_infusions(frame, codes=('FRN',), start='2021-01-01', end='2025-12-31', maximum=20000):
    df=frame.copy()
    code=df['product_code'].fillna('').astype(str).str.upper()
    dates=pd.to_datetime(df['date_received'],errors='coerce')
    return df[code.isin(codes) & dates.between(pd.Timestamp(start),pd.Timestamp(end))].head(maximum).reset_index(drop=True)

"""Download a configurable, date-filtered infusion-pump subset, never all MAUDE."""
import argparse
import json
from datetime import datetime, timezone
from config.settings import settings, path
from src.ingestion.openfda_client import OpenFDAClient

def download(maximum=None, start=None, end=None):
    cfg = settings()['data']
    maximum = maximum or cfg['max_rows']; start = start or cfg['start_date']; end = end or cfg['end_date']
    if start > end: raise ValueError('start must not exceed end')
    codes = ' OR '.join('device.device_report_product_code:'+c for c in cfg['product_codes'])
    query = f'({codes}) AND date_received:[{start.replace("-", "")} TO {end.replace("-", "")}]'
    dest = path('data/raw/maude_download.jsonl'); dest.parent.mkdir(parents=True,exist_ok=True)
    metadata = {'query':query,'requested':maximum,'downloaded':0,'complete':False,'retrieved_at':datetime.now(timezone.utc).isoformat(),'sampling':'date_received ascending, capped convenience sample','endpoint':'https://api.fda.gov/device/event.json'}
    manifest = dest.with_suffix('.manifest.json')
    try:
        with dest.open('w',encoding='utf-8') as f:
            for rows,_ in OpenFDAClient().pages('device/event',query,maximum,'date_received:asc'):
                for row in rows: f.write(json.dumps(row)+'\n')
                metadata['downloaded'] += len(rows)
                manifest.write_text(json.dumps(metadata,indent=2),encoding='utf-8')
        metadata['complete'] = True
    finally:
        manifest.write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(f'Saved {metadata["downloaded"]} records to {dest}. Process with src.ingestion.load_maude.')
    return dest
if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--max-rows',type=int);p.add_argument('--start');p.add_argument('--end');a=p.parse_args()
    download(a.max_rows,a.start,a.end)

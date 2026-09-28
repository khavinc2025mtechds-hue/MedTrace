"""Rules with evidence spans and local negation. No inferred patient diagnosis."""
import re
from src.preprocessing.clean_text import clean_text
PATTERNS={
'occlusion alarm':r'\bocclusion(?: alarm| alert)?\b',
'delivery interruption':r'\b(?:stopped (?:medication |drug |fluid |infusion )?delivery|delivery (?:stopped|interrupted)|infusion (?:stopped|interrupted)|underinfusion|under-infusion)\b',
'battery failure':r'\bbattery (?:fail\w*|deplet\w*|drain\w*|dead)\b',
'software issue':r'\b(?:software (?:error|fail\w*)|firmware (?:error|fail\w*)|reboot\w*|froze|frozen)\b',
'flow-rate issue':r'\b(?:overinfusion|over-infusion|incorrect flow|flow.rate (?:error|incorrect)|overdose|underdose)\b',
'alarm failure':r'\b(?:alarm (?:failed|failure|did not sound)|no alarm|false alarm)\b',
'mechanical failure':r'\b(?:broken|crack\w*|leak\w*|mechanical failure)\b',
'sensor issue':r'\bsensor (?:fail\w*|error|issue)\b',
'power failure':r'\b(?:power (?:fail\w*|loss)|unexpected shutdown|shut down)\b'}

def negated(text, start):
    prefix=re.split(r'[.!?;]|\bbut\b|\bhowever\b',text[:start],flags=re.I)[-1]
    return bool(re.search(r'\b(?:no|not|without|denies|denied)\b(?:\W+\w+){0,4}\W*$',prefix,re.I))

def extract(text: str, fields=None, use_spacy=False) -> dict:
    raw=clean_text(text);fields=fields or {};facts=[];categories=[]
    for category,pattern in PATTERNS.items():
        for m in re.finditer(pattern,raw,re.I):
            # 'No alarm' is itself positive evidence of an alarm issue.
            if m.group().lower()!='no alarm' and negated(raw,m.start()):continue
            categories.append(category);facts.append({'field':'problem','value':category,'quote':m.group(),'start':m.start(),'end':m.end(),'source':'complaint'})
    serious=[]
    for m in re.finditer(r'\b(?:death|died|serious injury|cardiac arrest|hospitali[sz](?:ed|ation))\b',raw,re.I):
        if not negated(raw,m.start()):serious.append(m.group());facts.append({'field':'severity_indicator','value':m.group(),'quote':m.group(),'start':m.start(),'end':m.end(),'source':'complaint'})
    model=re.search(r'\bmodel\s*[:#]?\s*([A-Za-z0-9][A-Za-z0-9._-]*)',raw,re.I)
    maker=re.search(r'\bmanufacturer\s*:\s*([^,;.]+)',raw,re.I)
    nlp_mode='regex rules'
    if use_spacy:
        try:
            import spacy
            doc=spacy.blank('en')(raw);tokens=[t.text for t in doc if not t.is_space];nlp_mode='spaCy tokenizer + rules'
        except ImportError:tokens=raw.split();nlp_mode='regex rules (spaCy unavailable)'
    else:tokens=raw.split()
    explicit_impact=clean_text(fields.get('patient_impact',''))
    return {'device':fields.get('device_name') or ('Infusion pump' if re.search(r'\b(?:infusion pump|pump)\b',raw,re.I) else 'Unknown'),
      'manufacturer':fields.get('manufacturer') or (maker.group(1).strip() if maker else ''),
      'model':fields.get('model') or (model.group(1) if model else ''),
      'problems':list(dict.fromkeys(categories)) or ['other'],
      'alarm_issue':any('alarm' in c for c in categories),
      'patient_impact':explicit_impact or ('Reported serious outcome indicator: '+', '.join(serious) if serious else 'Not reported'),
      'serious_outcome':bool(serious) or bool(re.search(r'\b(death|serious injury)\b',explicit_impact,re.I) and not re.search(r'\b(no|not|without)\b',explicit_impact,re.I)),
      'outcome':'Serious indicator reported' if serious else 'Unknown',
      'severity_indicators':serious,'evidence_spans':facts,'technical_terms':list(dict.fromkeys(categories)),
      'token_count':len(tokens),'method':nlp_mode,'limitations':['Rule extraction is not clinically validated.','Missing fields remain unknown.']}

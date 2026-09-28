"""Conservative text normalization that retains negation and redaction markers."""
import re
import unicodedata

def clean_text(value: object) -> str:
    if value is None or str(value).strip().lower() in {'nan', 'none', '<na>'}:
        return ''
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(value))).strip()

def normalize_name(value: object) -> str:
    return clean_text(value).casefold()

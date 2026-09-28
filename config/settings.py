"""Project-relative configuration. Secrets remain in environment variables."""
from pathlib import Path
import os
import yaml
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
def path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p

def settings() -> dict:
    config = path(os.getenv('MEDTRACE_CONFIG', 'config/config.yaml'))
    data = yaml.safe_load(config.read_text(encoding='utf-8'))
    data['retrieval']['backend'] = os.getenv('RETRIEVAL_BACKEND', data['retrieval']['backend'])
    data['workflow'] = os.getenv('WORKFLOW_BACKEND', data['workflow'])
    return data

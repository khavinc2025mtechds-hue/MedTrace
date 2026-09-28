"""Read-only openFDA client with retries and search-after pagination."""
import logging
import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
LOG = logging.getLogger(__name__)
BASE = 'https://api.fda.gov/'
class OpenFDAClient:
    def __init__(self, timeout: int = 45):
        self.timeout = timeout
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429,500,502,503,504], allowed_methods=['GET'])
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        self.session.headers['User-Agent'] = 'MedTrace-Academic/0.1'

    def pages(self, endpoint: str, search: str, maximum: int, sort: str | None = None):
        if maximum < 1:
            return
        url = BASE + endpoint.strip('/') + '.json'
        params = {'search': search, 'limit': min(1000, maximum)}
        if sort: params['sort'] = sort
        key = os.getenv('OPENFDA_API_KEY')
        if key: params['api_key'] = key
        seen_urls = set()
        count = 0
        while url and count < maximum:
            if urlparse(url).hostname != 'api.fda.gov':
                raise ValueError('Unexpected pagination host')
            if url in seen_urls: raise RuntimeError('Repeated pagination URL')
            seen_urls.add(url)
            response = self.session.get(url, params=params, timeout=self.timeout)
            if response.status_code == 404:
                error = response.json().get('error', {})
                if error.get('code') == 'NOT_FOUND': return
            response.raise_for_status()
            payload = response.json()
            rows = payload.get('results', [])[:maximum-count]
            if not rows: return
            yield rows, payload.get('meta', {})
            count += len(rows)
            # FDA provides a Link header containing the search_after continuation.
            links = {k.lower(): v for k,v in response.links.items()}
            url = links.get('next', {}).get('url')
            params = None
            if url and key:
                parsed = urlparse(url); q = dict(parse_qsl(parsed.query)); q['api_key'] = key
                url = urlunparse(parsed._replace(query=urlencode(q)))
            if not url and count < min(maximum, payload.get('meta', {}).get('results', {}).get('total', 0)):
                raise RuntimeError('FDA omitted continuation before requested count; use smaller date partitions.')

    def collect(self, endpoint: str, search: str, maximum: int = 100, sort: str | None = None) -> list:
        return [row for rows, _ in self.pages(endpoint, search, maximum, sort) for row in rows]

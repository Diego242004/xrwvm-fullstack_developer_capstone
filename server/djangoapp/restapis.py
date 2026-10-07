import os
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name('.env'))
backend_url = os.getenv('backend_url', 'http://localhost:3030')
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', 'http://localhost:5050/')


def get_request(endpoint, **kwargs):
    request_url = backend_url.rstrip('/') + '/' + endpoint.lstrip('/')
    try:
        response = requests.get(request_url, params=kwargs, timeout=15)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        print('Network exception occurred: {}'.format(error))
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url.rstrip('/') + '/analyze/' + quote(text, safe='')
    try:
        response = requests.get(request_url, timeout=15)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        print('Network exception occurred: {}'.format(error))
        return None


def post_review(data_dict):
    request_url = backend_url.rstrip('/') + '/insert_review'
    try:
        response = requests.post(request_url, json=data_dict, timeout=15)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        print('Network exception occurred: {}'.format(error))
        return None

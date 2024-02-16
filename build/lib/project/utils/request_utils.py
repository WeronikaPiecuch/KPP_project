import requests
from project.utils.constants import APIKEY, URL


def get_response(data_url, params):
    url = URL + data_url + '?'
    for key, value in params.items():
        url += f'{key}={value}&'
    url += f'apikey={APIKEY}'

    response = ''
    while True:
        try:
            response = requests.get(url, timeout=5)
            break
        except requests.exceptions.Timeout:
            continue

    return response.json()['result']

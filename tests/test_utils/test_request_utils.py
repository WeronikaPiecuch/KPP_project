import pytest
from unittest.mock import patch, MagicMock
from project.utils.constants import APIKEY, URL
from project.utils.request_utils import get_response
import requests


@pytest.fixture
def sample_params():
    return {'param1': 'value1', 'param2': 'value2'}


@pytest.fixture
def sample_data_url():
    return 'sample_data'


@pytest.fixture
def sample_response():
    return {'result': 'sample_result'}


def test_get_response_timeout(sample_params, sample_data_url, sample_response):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_response
        mock_get.side_effect = [requests.exceptions.Timeout, mock_response]

        result = get_response(sample_data_url, sample_params)

        expected_url = f'{URL}{sample_data_url}?param1=value1&param2=value2&apikey={APIKEY}'
        mock_get.assert_called_with(expected_url, timeout=5)
        assert mock_get.call_count == 2

        assert result == 'sample_result'

from io import BytesIO
import json
import pandas as pd
import pytest
from ..handler import app

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def simple_json_test(client, url):
    '''Just confirm Simple json conversts as per url contract.'''
    data = [{'info': 'Greate City',
            'shortname': 'FL',
            'state': 'Florida'},
            {'info': 'Nice Place!',
            'shortname': 'OH',
            'state': 'Ohio'}]
    response = client.post(url, data=json.dumps(data),
        content_type='application/json')
    output = BytesIO()
    output.write(response.data)
    # import pdb; pdb.set_trace()
    if 'excel' in url:
        df = pd.read_excel(output)
    else:
        df = pd.read_csv(output)
    assert len(df.columns) == len(data[0].keys())
    for idx, entry in enumerate(data):
        assert df['info'][idx] == data[idx]['info']
        assert df['shortname'][idx] == data[idx]['shortname']
        assert df['state'][idx] == data[idx]['state']


def nested_json_test(client, url):
    '''Just confirm nested json converts as per url contract.'''
    data = [{'info': {'governor': 'Rick Scott', 'vice_gov': 'Mike Jackson'},
            'shortname': 'FL',
            'state': 'Florida'},
            {'info': {'governor': 'John Kasich', 'vice_gov': 'Peter Parker'},
            'shortname': 'OH',
            'state': 'Ohio'}]
    response = client.post(url, data=json.dumps(data),
            content_type='application/json')
    output = BytesIO()
    output.write(response.data)
    if 'excel' in url:
        df = pd.read_excel(output)
    else:
        df = pd.read_csv(output)
    assert len(df.columns) == len(data[0].keys()) + 1 #extra 1 for nested entries
    for idx, entry in enumerate(data):
        assert df['info.governor'][idx] == data[idx]['info']['governor']
        assert df['info.vice_gov'][idx] == data[idx]['info']['vice_gov']
        assert df['shortname'][idx] == data[idx]['shortname']
        assert df['state'][idx] == data[idx]['state']


def test_simple_json_to_excel(client):
    simple_json_test(client, '/excel')

def test_simple_json_to_csv(client):
    simple_json_test(client, '/csv')

def test_nested_json_to_excel(client):
    nested_json_test(client, '/excel')

def test_nested_json_to_csv(client):
    nested_json_test(client, '/csv')

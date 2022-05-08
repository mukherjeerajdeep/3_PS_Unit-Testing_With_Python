import requests
from unittest import mock

'''
spec: This can be either a list of strings or an existing object (a class or instance) that acts as the 
specification for the mock object. If you pass in an object then a list of strings is formed by calling dir on the 
object (excluding unsupported magic attributes and methods). Accessing any attribute not in this list will raise an 
AttributeError. 

If spec is an object (rather than a list of strings) then _class_ returns the class of the spec object. This allows 
mocks to pass isinstance tests. 

spec_set: A stricter variant of spec. If used, attempting to set or get an attribute on the mock that isn’t on the 
object passed as spec_set will raise an AttributeError. 
'''

def test_mock_example():
    # The unittest mock() use case
    with mock.patch('requests.get') as mocker:
        resp_mock = mock.NonCallableMock(spec=requests.Response)
        resp_mock.json = mock.Mock(return_value={'hello': 'world'})
        resp_mock.headers = {'Content-Type': 'application/json'}
        mocker.return_value = resp_mock

        resp = requests.get('https://pycon-au.org')

        assert resp.json()['hello'] == 'world'
        assert resp.headers['Content-Type'] == 'application/json'
        assert mocker.called




import requests
import requests_mock


def test_requests_mock_example():
    with requests_mock.mock() as mocker:
        mocker.get('https://pycon-au.org',
                   json={'hello': 'world'},
                   headers={'Content-Type': 'application/json'},
                   status_code=400
                   )

        resp = requests.get('https://pycon-au.org')

        assert resp.json()['hello'] == 'world'
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.status_code == 400
        assert mocker.called


def test_requests_mock_circular():
    with requests_mock.mock() as mocker:
        a = mocker.post('https://pycon-au.org/a', text='bleh')
        b = mocker.get('https://pycon-au.org/b', text='PyConAU')
        c = mocker.get('https://pycon-au.org/c', text='2022')
        d = mocker.delete('https://pycon-au.org/d', text='Melbourne')
        e = mocker.get('https://pycon-au.org/e', text='Hello')

        responses = [requests.get('https://pycon-au.org/%s' % path)
                     for path in ('e', 'b', 'c')]

        for resp in responses:
            assert resp.status_code == 200

        print(" ".join(resp.text for resp in responses))

        for m in [e, b, c]:
            assert m.called_once


def test_what_passes_though_mocker():
    with requests_mock.mock() as mocker:
        m = mocker.post('https://pycon-au.org/a', text='Success')

        resp = requests.post('https://pycon-au.org/a?param=value',
                             headers={'Authorization': 'Token abcd'},
                             json={'Hello': 'World'})

        assert mocker.called_once
        assert mocker.called == True
        assert mocker.call_count == 2

        assert mocker.last_request.netloc == "pycon-au.org"
        assert mocker.last_request.path == '/a'
        assert mocker.last_request.verify
        assert mocker.last_request.json() == {'Hello': 'World'}
        assert mocker.last_request.headers['Authorization'] == 'Token abcd'
        assert mocker.last_request.qs['param'] == ['value']


def test_fail_lack_of_mocker():
    with requests_mock.mock() as mocker:
        resp = requests.post('https://pycon-au.org/a?param=value',
                             headers={'Authorization': 'Token abcd'},
                             json={'Hello': 'World'})

    assert Exception == "NoMockAddress"

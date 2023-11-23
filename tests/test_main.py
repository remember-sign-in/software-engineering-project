from . import client

def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == '"Hello World"'

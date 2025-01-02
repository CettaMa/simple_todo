import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302
    assert '/' in response.location

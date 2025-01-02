import pytest
import sys
import os
from flask import session

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_register(client):
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect to index
    with client.session_transaction() as sess:
        assert 'user' in sess
        assert sess['user'] == 'testuser'

def test_login(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect to index
    with client.session_transaction() as sess:
        assert 'user' in sess
        assert sess['user'] == 'testuser'

def test_logout(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to login
    with client.session_transaction() as sess:
        assert 'user' not in sess

def test_add_task(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/add', data={'task': 'New Task'})
    assert response.status_code == 302  # Redirect to index
    assert b'New Task' in client.get('/').data

def test_complete_task(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/add', data={'task': 'New Task'})
    response = client.post('/complete/0')
    assert response.status_code == 302  # Redirect to index
    response = client.get('/')
    assert b'New Task' not in response.data  # Task should not be in ongoing tasks
    assert b'<li class="task"><span>New Task</span>' in response.data  # Task should be in completed tasks

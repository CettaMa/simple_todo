import pytest
import sys
import os
import logging
from flask import session
import time

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_register(client):
    logger.info("Testing user registration")
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect to index
    with client.session_transaction() as sess:
        assert 'user' in sess
        assert sess['user'] == 'testuser'
    logger.info("User registration test passed")

def test_login(client):
    logger.info("Testing user login")
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect to index
    with client.session_transaction() as sess:
        assert 'user' in sess
        assert sess['user'] == 'testuser'
    logger.info("User login test passed")

def test_logout(client):
    logger.info("Testing user logout")
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to login
    with client.session_transaction() as sess:
        assert 'user' not in sess
    logger.info("User logout test passed")

def test_add_task(client):
    logger.info("Testing adding a new task")
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/add', data={'task': 'New Task'})
    assert response.status_code == 302  # Redirect to index
    response = client.get('/')
    assert b'New Task' in response.data  # Task should be in ongoing tasks
    logger.info("Add task test passed")

def test_complete_task(client):
    logger.info("Testing completing a task")
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/add', data={'task': 'New Task'})
    response = client.post('/complete/0')
    assert response.status_code == 302
    response = client.get('/')
    with open('response.html', 'wb') as f:
        f.write(response.data)
    expected_html = b"""
        <h2>Completed Tasks</h2>
        
            <ul>
                
                    <li class="task">
                        <span>New Task</span>
                        <form method="POST" action="/delete_completed/0">
                            <button type="submit">Delete</button>
                        </form>
                    </li>
                
            </ul>
        

    """
    assert expected_html in response.data  # Task should be in completed tasks
    logger.info("Complete task test passed")

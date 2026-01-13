import sys
import os
import pytest
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from src.app import *

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_user(client):
    response = client.post("/submit", data={
        'username': 'TestUser',
        'language': 'Polish'
    }, follow_redirects=True)
    
    assert response.status_code == 200

    user = User.query.filter_by(username='TestUser').first()
    
    assert user is not None
    assert user.language == 'Polish'
    db.session.delete(user)
    db.session.commit()

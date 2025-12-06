import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_login_register(client):
    response = client.post("/register", json = {"username" : "hugoo", "password" : "Hugo@1234", "confirm" : "Hugo@1234"}, follow_redirects=True)
    assert response.status_code == 201

    response = client.post("/login", json = {"username" : "hugoo", "password" : "Hugo@1234"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_create_task(client):
    client.post("/register", json = {"username" : "hugoo", "password" : "Hugo@1234", "confirm" : "Hugo@1234"}, follow_redirects=True)
    client.post("/login", json = {"username" : "hugoo", "password" : "Hugo@1234"}, follow_redirects=True)
    response = client.post("/tasks/new", data = {"title" : "Task", "description" : "description", "due_date" : "2025-12-07"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Task created." in response.data

def test_editing_toggling_task(client):
    client.post("/register", json = {"username" : "hugoo", "password" : "Hugo@1234", "confirm" : "Hugo@1234"}, follow_redirects=True)
    client.post("/login", json = {"username" : "hugoo", "password" : "Hugo@1234"}, follow_redirects=True)
    client.post("/tasks/new", data = {"title" : "Task"})

    response = client.post("/tasks/1/toggle", follow_redirects=True)

    assert response.status_code == 200
    assert b"Task status updated" in response.data

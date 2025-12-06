import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_login_register(client):
    response = client.post("/register", json = {"username" : "hugo", "password" : "hugo1"})
    assert response.status_code == 201

    response = client.post("/login", json = {"username" : "hugo", "password" : "hugo1"})
    assert response.status_code == 200

def test_create_task(client):
    client.post("/register", json = {"username" : "hugo", "password" : "hugo1"})
    login = client.post("/login", json = {"username" : "hugo", "password" : "hugo1"})
    login.json["token"]

    response = client.post("/tasks", json = {"title" : "give tp"})

    assert response.status_code == 201
    assert response.json["title"] == "give tp"

def test_editing_toggling_task(client):
    client.post("/register", json = {"username" : "hugo", "password" : "hugo1"})
    login = client.post("/login", json = {"username" : "hugo", "password" : "hugo1"})
    login.json["token"]

    task = client.post("/tasks", json = {"title" : "give tp"})
    taskID = task.json["id"]
    toggle_task = client.put(f"/tasks/{taskID}/toggle")

    assert toggle_task.status_code == 200
    assert toggle_task.json["completed"] is True

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_chat_with_valid_message(client):
    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "response" in data
    assert "state" in data


def test_chat_with_missing_message(client):
    response = client.post(
        "/chat",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_chat_with_null_message(client):
    response = client.post(
        "/chat",
        json={
            "message": None
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Message cannot be empty."


def test_chat_with_non_string_message(client):
    response = client.post(
        "/chat",
        json={
            "message": 123
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Message must be a string."


def test_chat_with_empty_message(client):
    response = client.post(
        "/chat",
        json={
            "message": ""
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Message cannot be empty."


def test_chat_with_whitespace_message(client):
    response = client.post(
        "/chat",
        json={
            "message": "     "
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Message cannot be empty."


def test_chat_with_json_array(client):
    response = client.post(
        "/chat",
        json=[
            "Hello"
        ]
    )

    assert response.status_code == 400


def test_chat_with_json_string(client):
    response = client.post(
        "/chat",
        json="Hello"
    )

    assert response.status_code == 400


def test_chat_without_json(client):
    response = client.post(
        "/chat",
        data="Hello",
        content_type="text/plain"
    )

    assert response.status_code == 415


def test_chat_with_malformed_json(client):
    response = client.post(
        "/chat",
        data='{"message": ',
        content_type="application/json"
    )

    assert response.status_code == 400


def test_reset_chat(client):
    response = client.post("/reset")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Conversation reset successfully."
    assert "state" in data

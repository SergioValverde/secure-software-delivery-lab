from fastapi.testclient import TestClient

from secure_delivery_lab.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_endpoint() -> None:
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}


def test_create_and_retrieve_message() -> None:
    create_response = client.post(
        "/messages",
        json={"content": "   Deployment failed   "},
    )

    assert create_response.status_code == 201

    created_message = create_response.json()
    assert created_message["id"] > 0
    assert created_message["content"] == "Deployment failed"

    get_response = client.get(f"/messages/{created_message['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created_message


def test_missing_message_returns_404() -> None:
    response = client.get("/messages/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}


def test_unexpected_field_is_rejected() -> None:
    response = client.post(
        "/messages",
        json={
            "content": "Hello",
            "admin": True,
        },
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(
        error["type"] == "extra_forbidden"
        and error["loc"] == ["body", "admin"]
        for error in errors
    )


def test_whitespace_only_content_is_rejected() -> None:
    response = client.post(
        "/messages",
        json={"content": "     "},
    )

    assert response.status_code == 422


def test_content_over_200_characters_is_rejected() -> None:
    response = client.post(
        "/messages",
        json={"content": "A" * 201},
    )

    assert response.status_code == 422

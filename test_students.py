from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_crud_flow():
    payload = {
        "name": "Demo Student",
        "date_of_birth": "2006-05-10",
        "email": "demo.student@example.com",
        "phone": "9999999999",
        "course": "Computer Science (AIML)",
        "address": "Raipur",
        "enrollment_date": "2026-07-01",
    }
    created = client.post("/students", json=payload)
    assert created.status_code == 201
    student_id = created.json()["student_id"]

    fetched = client.get(f"/students/{student_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Demo Student"

    updated = client.patch(f"/students/{student_id}", json={"course": "AI & ML"})
    assert updated.status_code == 200
    assert updated.json()["course"] == "AI & ML"

    deleted = client.delete(f"/students/{student_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/students/{student_id}")
    assert missing.status_code == 404

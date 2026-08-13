def test_create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Dr. Smith"


def test_get_doctors(client):
    client.post(
        "/doctors",
        json={
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        },
    )

    response = client.get("/doctors")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_doctor(client):
    create_response = client.post(
        "/doctors",
        json={
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        },
    )

    doctor_id = create_response.json()["id"]

    response = client.get(f"/doctors/{doctor_id}")

    assert response.status_code == 200
    assert response.json()["id"] == doctor_id


def test_missing_doctor(client):
    response = client.get("/doctors/999")

    assert response.status_code == 404

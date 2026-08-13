def test_get_doctors(client):
    response = client.get("/doctors")

    assert response.status_code == 200
    assert response.json() == []


def test_create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr Smith",
            "specialization": "Cardiology",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Dr Smith"
    assert data["specialization"] == "Cardiology"


def test_get_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr Smith",
            "specialization": "Cardiology",
        },
    )

    doctor_id = response.json()["id"]

    response = client.get(f"/doctors/{doctor_id}")

    assert response.status_code == 200
    assert response.json()["id"] == doctor_id


def test_doctor_not_found(client):
    response = client.get("/doctors/999")

    assert response.status_code == 404

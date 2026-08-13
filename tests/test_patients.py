def test_get_patients(client):
    response = client.get("/patients")

    assert response.status_code == 200
    assert response.json() == []


def test_create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "John",
            "email": "john@example.com",
            "phone": "1234567890",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John"
    assert data["email"] == "john@example.com"
    assert data["phone"] == "1234567890"


def test_get_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "John",
            "email": "john@example.com",
            "phone": "1234567890",
        },
    )

    patient_id = response.json()["id"]

    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json()["id"] == patient_id


def test_patient_not_found(client):
    response = client.get("/patients/999")

    assert response.status_code == 404


def test_duplicate_patient_email(client):
    patient = {
        "name": "John",
        "email": "john@example.com",
        "phone": "1234567890",
    }

    response = client.post("/patients", json=patient)
    assert response.status_code == 201

    response = client.post("/patients", json=patient)

    assert response.status_code == 409

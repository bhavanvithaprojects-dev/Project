def test_create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


def test_get_patients(client):
    client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    response = client.get("/patients")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_patient(client):
    create_response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    patient_id = create_response.json()["id"]

    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json()["id"] == patient_id


def test_get_missing_patient(client):
    response = client.get("/patients/999")

    assert response.status_code == 404


def test_duplicate_patient_email(client):
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
    }

    assert client.post("/patients", json=payload).status_code == 201

    response = client.post("/patients", json=payload)

    assert response.status_code == 409

def create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "John",
            "email": "john@example.com",
            "phone": "1234567890",
        },
    )

    return response.json()["id"]


def create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr Smith",
            "specialization": "Cardiology",
        },
    )

    return response.json()["id"]


def test_get_appointments(client):
    response = client.get("/appointments")

    assert response.status_code == 200
    assert response.json() == []


def test_create_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id


def test_get_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    appointment_id = response.json()["id"]

    response = client.get(f"/appointments/{appointment_id}")

    assert response.status_code == 200
    assert response.json()["id"] == appointment_id


def test_appointment_not_found(client):
    response = client.get("/appointments/999")

    assert response.status_code == 404


def test_invalid_appointment_range(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T11:00:00",
            "appointment_end": "2026-08-20T10:00:00",
        },
    )

    assert response.status_code == 422


def test_patient_not_found_for_appointment(client):
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": 999,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert response.status_code == 404


def test_doctor_not_found_for_appointment(client):
    patient_id = create_patient(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": 999,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert response.status_code == 404


def test_overlapping_appointment_is_rejected(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:30:00",
            "appointment_end": "2026-08-20T11:30:00",
        },
    )

    assert second.status_code == 409


def test_appointment_after_previous_one_is_allowed(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T11:00:00",
            "appointment_end": "2026-08-20T12:00:00",
        },
    )

    assert second.status_code == 201

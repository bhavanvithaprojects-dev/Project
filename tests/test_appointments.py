def create_patient(client):
    return client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    ).json()["id"]


def create_doctor(client):
    return client.post(
        "/doctors",
        json={
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        },
    ).json()["id"]


def appointment_payload(patient_id, doctor_id, start, end):
    return {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_start": start,
        "appointment_end": end,
    }


def test_create_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T10:00:00",
            "2026-08-13T11:00:00",
        ),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id


def test_get_appointments(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T10:00:00",
            "2026-08-13T11:00:00",
        ),
    )

    response = client.get("/appointments")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    create_response = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T10:00:00",
            "2026-08-13T11:00:00",
        ),
    )

    appointment_id = create_response.json()["id"]

    response = client.get(f"/appointments/{appointment_id}")

    assert response.status_code == 200
    assert response.json()["id"] == appointment_id


def test_missing_appointment(client):
    response = client.get("/appointments/999")

    assert response.status_code == 404


def test_overlapping_appointment_is_rejected(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T10:00:00",
            "2026-08-13T11:00:00",
        ),
    )

    assert first.status_code == 201

    overlapping = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T10:30:00",
            "2026-08-13T11:30:00",
        ),
    )

    assert overlapping.status_code == 409


def test_back_to_back_appointment_is_allowed(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T10:00:00",
            "2026-08-13T11:00:00",
        ),
    )

    assert first.status_code == 201

    second = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T11:00:00",
            "2026-08-13T12:00:00",
        ),
    )

    assert second.status_code == 201


def test_invalid_appointment_range(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json=appointment_payload(
            patient_id,
            doctor_id,
            "2026-08-13T12:00:00",
            "2026-08-13T11:00:00",
        ),
    )

    assert response.status_code == 422

def test_get_all_planets_with_no_record(client):

    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_specific_planets(client, one_planet):

    id = one_planet.id
    response = client.get(f"/planets/{id}")
    response_body = response.get_json()

    assert response.status_code == 200

    assert response_body["id"] == one_planet.id
    assert response_body["name"] == one_planet.name
    assert response_body["description"] == one_planet.description
    assert response_body["num_moons"] == one_planet.number_of_moons


def test_get_specific_planets_not_found(client):
    response = client.get("/planets/1000")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Planet 1000 not found"}


def test_create_planets_successfully(client):
    response = client.post(
        "/planets",
        json={
            "name": "Mercury",
            "description": "Smallest rocky planet, closest to the Sun",
            "num_moons": 0,
        },
    )

    response_body = response.get_json()

    assert response.status_code == 201

    assert response_body["name"] == "Mercury"
    assert response_body["description"] == "Smallest rocky planet, closest to the Sun"
    assert response_body["num_moons"] == 0

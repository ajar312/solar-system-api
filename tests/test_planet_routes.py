def test_get_all_planets_with_no_records(client): 
    #Act
    response = client.get("/planets")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_planet_succeeds(client, two_saved_planets):
    response = client.get("planets/1")
    response_body=response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Mercury", 
        "description": "The closest planet to the Sun", 
        "color": "Gray"
    }

def test_create_one_planet(client):
    response = client.post("/planets", json={
        "name": "Pluto",
        "description": "A dwarf planet with a varied surface",
        "color": "A rainbow of pale blues, yellows, oranges, and deep reds"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Pluto",
        "description": "A dwarf planet with a varied surface",
        "color": "A rainbow of pale blues, yellows, oranges, and deep reds"
    }

def test_get_one_planet_not_found(client):
    response = client.get('/planets/10') 
    assert response.status_code == 404
    assert response.get_json() == {"message": "planet 10 not found"}
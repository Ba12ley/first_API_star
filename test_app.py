from apistar import test
from main import app, cars

client = test.TestClient(app)

def test_list_cars():
    response = client.get('/')
    assert response.status_code == 200
    cars = response.json()
    assert len(cars) == 1000

def test_create_car():
    car_count = len(cars)
    data = {
        'car_make': 'Ford',
        'car_model': 'Ka',
        'year': 2000,
        'vin': '368'
    }

    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(cars) == car_count +1

    #Check for persistence

    response = client.get('/1001/')
    expected = {
        'id': 1001,
        'car_make': 'Ford',
        'car_model': 'Ka',
        'year': 2000,
        'vin': '368'
    }
    assert response.json() == expected

def test_delete_car():
    car_count = len(cars)
    response = client.delete(f'/2/')

    assert response.status_code == 204
    assert len(cars) == car_count -1

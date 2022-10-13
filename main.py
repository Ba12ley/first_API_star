import json
from typing import List
from apistar import App, Route, types, validators
from apistar.http import JSONResponse


def _load_data():
    with open('MOCK_DATA.json') as f:
        cars = json.loads(f.read())
        return {car["id"]: car for car in
                cars}  # As a dict instead of list.  List of dicts would be less efficient to search


cars = _load_data()
VALID_MANUFACTURER = set([car["car_make"] for car in cars.values()])

CAR_NOT_FOUND = 'Car not found'


class Car(types.Type):
    id = validators.Integer(allow_null=True)  # when assigned in POST
    car_make = validators.String(enum=list(VALID_MANUFACTURER))
    car_model = validators.String(max_length=50)
    year = validators.Integer(minimum=1900, maximum=2022)
    vin = validators.String(max_length=50, default='')


# API Handlers. With type hints

def list_cars() -> List[Car]:
    return [Car(car[1]) for car in sorted(cars.items())]  # list comprehension


def create_car(car: Car) -> JSONResponse:
    car_id = max(cars.keys()) + 1
    car.id = car_id
    cars[car_id] = car
    return JSONResponse(Car(car), status_code=201)


def get_car(car_id: int) -> JSONResponse:
    car = cars.get(car_id)
    if not car:
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    return JSONResponse(Car(car), status_code=200)


def update_car(car_id: int, car: Car) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    else:
        car.id = car_id
        cars[car_id] = car
        return JSONResponse(Car(car), 200)


def delete_car(car_id: int) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    else:
        del cars[car_id]
        return JSONResponse({}, 204)


# Specify endpoint method and handler
routes = [
    Route('/', method='GET', handler=list_cars),
    Route('/', method='POST', handler=create_car),
    Route('/{car_id}/', method='GET', handler=get_car),
    Route('/{car_id}/', method='PUT', handler=update_car),
    Route('/{car_id}/', method='DELETE', handler=delete_car),
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)

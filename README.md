
# Nuvolar Airlines

A REST API to perform CRUD operations on a fleet via an airline management system.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## API Reference
### Below is a list of all vital endpoints. To view all the other endpoints, please visit the API docs at `localhost:8000/api/docs/`

#### Get all flights

```
  GET /api/airspace/flights/
```


#### Get single flight

```
  GET /api/airspace/<flight_public_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `flight_public_id`      | `string` | **Required**. Id of flight to fetch |

#### Create a flight

```
  POST /api/airspace/flights/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `departure_time`      | `date` | **Required**. Datetime of the flight (departure) |
| `arrival_time`      | `date` | **Required**. Datetime of the flight (arrival) |
| `departure_airport`      | `UUID` | **Required**. Public ID of an airport |
| `arrival_airport`      | `UUID` | **Required**. Public ID of an airport |

#### Add an aircraft to a flight

```
  POST /api/airspace/flights/<flight_public_id>/add-aircraft/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `aircraft`      | `UUID` | **Required**. Public ID of an aircraft |

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `flight_public_id`      | `UUID` | **Required**. Public ID of a flight |


#### Generate Report
```
  POST /api/airspace/flights/generate-report/
```
| Query Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `departure_time`      | `UUID` | **Required**. Departure time of flight range |
| `arrival_time`        | `UUID` | **Required**. Arrival time of flight range

## Run Locally

Clone the project

```bash
  git clone git@github.com:f-gozie/nuvolar-airlines.git
```

Go to the project directory

```bash
  cd nuvolar_airlines
```

Build the docker containers (assuming you have docker installed)

```bash
  make build
```

Start the server

```bash
  make up
```

Load the airports (Optional)

```bash
  make populate-airports
```


## Authors

- [@f-gozie](https://www.github.com/f-gozie)


## Features

- Ability to filter flights within a date range
- Ability to populate airports using Aviation Stack API
- Ability to generate reports of flight analytics
- Ability to optionally store the results of the report in the database (async)

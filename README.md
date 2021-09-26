# Personal Spending Tracker API

[![](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

SUTD 50.012 Networks Lab 2

## Checkoff

TA please refer to [demo](demo) for checkoff demo.

## Development

### Run MongoDB and API services in containers

0. Install [**docker**](https://docs.docker.com/engine/install/) & [**docker-compose**](https://docs.docker.com/compose/install/).

1. Build and run containers using docker-compose
    ```bash
    docker-compose up --build
    ```
2. Stop and remove containers
    ```bash
    docker-compose down
    ```

Check API documentation after firing up local server

-   Go to [127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

## Disclaimers

-   [MIT License](LICENSE) Copyright (c) 2021
-   This application is developed to fulfill the course requirement (Lab 2) of SUTD 50.012 Networks (2021 Fall).

## Acknowledgement

-   Docker image: [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

# Personal Spending Tracker API

[![](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

SUTD 50.012 Networks Lab 2

## Checkoff

TA, please refer to the [demo](demo) folder for checkoff instructions.

## Development

### Run MongoDB and API services in containers

0.  Install [**docker**](https://docs.docker.com/engine/install/) & [**docker-compose**](https://docs.docker.com/compose/install/).

1.  Build and run containers using docker-compose
    ```bash
    # at project root
    docker-compose up --build
    ```
    Check API documentation after firing up local server
    -   Go to [127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
2.  Stop and remove containers
    ```bash
    # at project root
    docker-compose down
    ```
3.  Delete all local data and local cache
    ```bash
    # at project root
    make clean
    ```

## Disclaimers

-   [MIT License](LICENSE) Copyright (c) 2021
-   This application is developed to fulfill the course requirement (Lab 2) of SUTD 50.012 Networks (2021 Fall).

## Acknowledgement

-   Docker image: [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

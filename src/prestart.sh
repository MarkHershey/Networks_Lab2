#!/usr/bin/env bash

# update pip
printf "\n>>> pip3 install --upgrade pip wheel setuptools \n"
pip install --upgrade pip wheel setuptools
printf ">>> \xE2\x9C\x94 OK \n"


# install project dependencies
printf "\n>>> pip3 install project dependencies...\n"
pip install puts==0.0.4
pip install --upgrade bcrypt pyjwt fastapi passlib requests pytest uvicorn dnspython pymongo aiofiles python-multipart
printf ">>> \xE2\x9C\x94 OK \n"
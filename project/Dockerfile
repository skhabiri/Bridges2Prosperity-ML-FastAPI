# pull official base image, python:3.8-slim-buster
FROM python:3.8-slim-buster

# set the working directory in container to /usr/src/app
WORKDIR /usr/src/app

# install pip for python3.8 in the custom image
RUN python -m pip install --upgrade pip

# copy requirements.txt from current directory in docker host to WORKDIR in the image
COPY ./requirements.txt .


# install python dependencies
RUN pip install -r requirements.txt

# copy everything from docker host current directory to the WORKDIR image (adding app)
COPY . .


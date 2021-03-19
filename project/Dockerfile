# This Dockerfile is used to create "apiwebapp" service image 
# This is defined in docker-compose.yml

# pull official base image, python:3.8-slim-buster from docker-hub
FROM python:3.8-slim-buster

# set the working directory in container to /usr/src/b2p/project
# "/usr/src/" is for container. "/b2p/project" name is arbitrary
WORKDIR /usr/src/b2p/project

# install pip for python3.8 in the custom image
RUN python -m pip install --upgrade pip

# copy "requirements.txt" from docker host current directory, into the WORKDIR in the container
# docker host dir is usually where Dockerfile is located. That is specified by a service "context"
COPY ./requirements.txt .

# install python dependencies
RUN pip install -r ./requirements.txt

# copy everything from docker host curren directory "./project" to the WORKDIR image
COPY . .


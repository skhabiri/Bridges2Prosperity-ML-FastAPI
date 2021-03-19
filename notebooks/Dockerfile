# This Dockerfile is used to create "ipynotebook" service image 
# this is defined in "docker-compose.yml"

# pull base image from "apiwebapp" service docker image 
# This allows to include all the installed packages 
# of "apiwebapp" docker image in this container as well
FROM b2p/fastapi-app

# set the working directory in container to /usr/src/b2p/notebooks
WORKDIR /usr/src/b2p/notebooks

# install pip for its base python (3.8) in the ipynotebook image
RUN python -m pip install --upgrade pip

# copy "requirements.txt" from docker host current directory, into the WORKDIR in the container
# docker host dir is usually where Dockerfile is located. That is specified by a service "context"
COPY ./requirements.txt .

# install additional requirements
#RUN pip install jupyterlab
RUN pip install -r ./requirements.txt

# copy everything from docker host (path is relative to "context") dir of the 
# service that calls this Dockerfile to the WORKDIR image
COPY . .
COPY ../Data/ /usr/src/b2p/Data/


# Welcome to our Repo! 
[![Welcome Video](https://imgur.com/7gaai5K.png)](https://youtu.be/1qVVODfPtto)

# Links to Deployments
<p>&nbsp;</p>

[Docs](https://docs.labs.lambdaschool.com/data-science/)

[Latest deployment](https://lab28dsk.bridgestoprosperity.dev/)

[Previous deployment](https://b2pmergefinal.bridgestoprosperity.dev/)

[Deployed API](https://d-ds.bridgestoprosperity.dev/) 

[Deployed API#2](https://d-ds-labs28.bridgestoprosperity.dev )

# Architeture

![Welcome Video](https://github.com/Lambda-School-Labs/bridges-to-prosperity-ds-d/blob/main/assets/Flowchart.png)

# Setting up the Project:
First clone the repository to your local machine
```
git clone https://github.com/skhabiri/bridges-to-prosperity-b2p.git
```
global git configuration is in `~/.gitconfig` and the project config is set in `.git/config`. We can check the global git config by: `git config --global --get user.name` and `git config --global --get user.email`. In order to config only the project git account, use:

```
git config user.email <user_email>
git config user.name <git_username>
```
# Virtual Environment:
We can either use `pipenv` or `docker` to reproduce the environment.

### pipenv
cd to the repo directory and install dependencies. In general `Pipfile` supercede requirements.txt. However, if you only have a requirements.txt file available when running `pipenv install --dev`, pipenv will automatically import the contents of this file and create a Pipfile for you. Or you could be specific with `pipenv install -r path/to/requirements.txt` to import a requirements file. 
Now activate the virtual environment with `pipenv shell`.
To work with the notebook you can create a ipykernel from the env and launch jupyter in env with `pipenv run jupyter notebook`. For working with .py files in IDE you can use VS Code by running `code .`. Make sure you have the Python extension in **View → Extensions**. Now activate the env by **View → Command Palette → Python: Select Interpreter**

Instead of pipenv we can use Docker to run our app in an isolated disposable container.

### Docker
For building a docker image we need Dockerfile which specifies: the base python to use, working directory on the image volume, all the package dependencies, and the files (web app) that needs to be copied from the host container to the image.
In this approach we build an image based on a python version and packagees specified in requirements.txt. We also map the local volume to the container volume that will be created based on this image. Additionally using docker-compose would allow us to run some services such as web server inside the container. For that we would need to define the networking ports, volume mapping and point of entry command to run. Here are the files that we need to build the image and compose multiple services into one container.

#### Dockerfile

This file is used to build a custom image. 
```
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
```
docker-compose allows to have a container composed of multiple services. We use docker-compose.yml to define the services, entry point command, volume and network port mapping from the docker host to the container.

#### docker-compose.yml 
The Compose file is a YAML file defining services such as web and volumes and networks for a Docker application.
```
version: '3.7'
services:
  web:
    # The web service uses an image that’s built from the Dockerfile located in the ./project directory.
    build: ./project
    
    #entry point for docker-compose up
    command: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

    # mounts volume ./project to container's /usr/src/app path
    volumes:
      - ./project:/usr/src/app
    
    # maps container port 8000 to TCP port 80 on the docker host and from there to the outside world
    ports:
      - 80:8000
```
mounting ./project directory on the host to /use/src/app inside the container, allows modifying the code on the fly, without having to rebuild the image, as the container gets updated in real time.
from the directory with docker-compose.yml we build the docker services image:
```
docker-compose build #builds the images, does not start the containers
docker-compose up #builds the images if the images do not exist and starts the container
docker-compose up --build #forced to build the images even when not needed and starts the containers
```
To list the images used to create containers, use `docker-compose images`. You won't need to rebuild when you update your code. You'll only need to rebuild if you update your requirements.txt or Dockerfile.

Now we can locally launch the web service in docker container with `docker-compose up`.

enter http://0.0.0.0:80 in web browser to launch the API locally








# How to Create DataBase Hosted in AWS 
- Log In w/ Credentials to AWS
- Relational DataBase Section
- Click Create DataBase, choose desired database, ex) PostGres
- Configure Settings, Make Password, Username
- Connect with pgadmin, datagrip
- TIP: Allow public access, create security groups incase you have trouble connecting via your domain

# How to Connect to data Base
- Save secret in .env file into 
- Create connection, cursor to the database using psycopg2
- Can make a function that constructs connections via function or simply type connections explicitly
```python
    def conn_curs():
        """
        makes a connection to the database
        """
        global db_name
        global db_user
        global db_password
        global db_host
        global db_port
        
        connection = psycopg2.connect(dbname=db_name, user= db_user,
                                      password=db_password, host= db_host,port=db_port)
        cursor = connection.cursor()
        return connection, cursor
```
# How to upload Data Frame as SQL Table to DataBase
- Convert CSV/Excel into DataFrame format : 
```python 
   #Make sure your file location does actually coresspond to a  working link
   df = pd.read("file_location")
```
- Upload DataFrame to SQL Table
```python   
   table_name = 'table_name'
   df.to_sql(table_name, con)
```
- Test SQL Table that is connected to DataBase.
- Check out Bridges_2_Prosperity_Final_Merged_DataFrameToPostgresSQL.ipynb notebook to see an example.

## Test Queries to Table B2P_oct_2018

```python
    
    # Testing Query to get Records based on Bridge Naem
    conn, cursor = conn_curs()
    query  = """SELECT "Bridge_Name" from public."B2P_oct_2018" where "Bridge_Name" = 'Bukinga' LIMIT 1;"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close
```

# How to Run App Locally
- Make sure u have a local.env file with proper secrets
- Save your .env file in the following location: project/app/api/.env 
- Go to your terminal run: docker-compose up







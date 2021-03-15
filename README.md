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

# Docker Compose

### Dockerfile
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

### docker-compose.yml 
defines different services such as web and volume.
```
version: '3.7'
services:
  web:
    # The web service uses an image that’s built from the Dockerfile located in the ./project directory.
    build: ./project
    
    command: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

    # mounts volume ./project to container's /usr/src/app path
    volumes:
      - ./project:/usr/src/app
    
    # maps container port 8000 to TCP port 80 on the docker host and from there to the outside world
    ports:
      - 80:8000
```
mounting ./project directory on the host to /use/src/app inside the container, allows modifying the code on the fly, without having to rebuild the image, as the container gets updated in real time.


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







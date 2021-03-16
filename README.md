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
Use [Whimsical](https://whimsical.com/) account.
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


# AWS
AWS is a cloud platform that offers various services. SOme the most important one for us:

#### AWS EC2
`Amazon Elastic Compute Cloud` (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers. Amazon EC2’s simple web service interface allows you to obtain and configure capacity with minimal friction. This is like virtual private servers.

#### AWS Elastic Beanstalk
AWS Elastic Beanstalk is an easy-to-use service for deploying and scaling web applications and services developed with Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker on familiar servers such as Apache, Nginx, Passenger, and IIS.
You can upload your code and Elastic Beanstalk automatically handles the deployment, from capacity provisioning, load balancing, auto-scaling to application health monitoring.

#### AWS RDS
To set up, operate, and scale a relational database in the cloud. Amazon RDS is a `Relational Database Service` that handles MySQL, Oracle or Microsoft SQL Server database engine. This means that the code, applications, and tools you already use today with your existing databases can be used with Amazon RDS. Amazon RDS automatically patches the database software and backs up your database, storing the backups for a user-defined retention period and enabling point-in-time recovery. You benefit from the flexibility of being able to scale the compute resources or storage capacity associated with your Database Instance (DB Instance) via a single API call. Some of the features offered by Amazon RDS are:
- Pre-configured Parameters
- Monitoring and Metrics
- Automatic Software Patching

#### AWS EBS
EBS is a virtual hard drive that you connect to your EC2 instance. Amazon `Elastic Block Store` (EBS) is a high-performance, block-storage service designed for use with Amazon Elastic Compute Cloud (EC2) for both throughput and transaction intensive workloads at any scale. A broad range of workloads, such as relational and non-relational databases, enterprise applications, containerized applications, big data analytics engines, file systems, and media workflows are widely deployed on Amazon EBS.

#### AWS S3 
S3 provides standalone storage. You can store and retrieve any amount of data, at any time, from anywhere on the web. `Amazon Simple Storage Service` provides a fully redundant data storage infrastructure for storing and retrieving any amount of data, at any time, from anywhere on the web.  You don't need to run an EC2 instance. and S3 is basically a hard drive with no computer and henece no processing of data. Use this to store images and other assets for websites. Keep backups and share files between services. Host static websites. Also, many of the other AWS services write and read from S3.

Amazon RDS belongs to `SQL Database as a Service` category of the tech stack, while Amazon S3 can be primarily classified under `Cloud Storage`.
Amazon S3 provides the following key features:
- Write, read, and delete objects of any size. The number of objects you can store is unlimited.
- Each object is stored in a bucket and retrieved via a unique, developer-assigned key.
- A bucket can be stored in one of several Regions. You can choose a Region to optimize for latency, minimize costs, or address regulatory requirements.

#### Route53
To set up the DNS records for a domain.

#### Install AWS CLI (Command Line Interface):
Install the aws cli from [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html). Check that the aws cli is installed by `which aws`.

#### Install AWS Elastic Beanstalk CLI
Use `pip install awsebcli` for that and check the successful installation with `eb --version`. Later on we'll use that to deploy Docker image to AWS elastic beanstalk.

#### Sign into your aws account
Make sure to choose us-east-1 region, and create a IAM user for the app instead of using the root credentials. You would also want to take a note of the secret access key, access key id and the account id or create an account alias.

#### Configure AWS CLI
use `aws configure` to enter the credentials. Those data are saved in `~/.aws/credentials` and `~/.aws/config`.

#### Building:
As a part of data science team the task is to train the model, deploy model in the cloud, and integrate machine learning into web product, using this tech stack:
* FastAPI: Web framework. Like Flask, but faster, with automatic interactive docs.
* AWS RDS Postgres: Relational database service. Like ElephantSQL.
* AWS Elastic Beanstalk: Platform as a service, hosts your API. Like Heroku.
* Docker: Containers, for reproducibility. Like virtual environments, but more reproducible.


#### Create security group
In EC2 service create a `security group`. This will be use when creating the database. In the `Inbound rules` section, click the `Add rule` button. For `Type`, select `PostgreSQL`. For `Source`, select `Anywhere`.

#### Create databas
Go to the RDS service. Click the `Create database` button. Select the following options:
* Database creation method = Standard create
* Engine type = PostgreSQL
* Template = Free tier
* DB instance identifier = you make up a name
* Master username = make up a name
* Master password = you make up a password
Scroll down to the `Connectivity` section, and select the following options:
* Public access = Yes
* VPC security group = Choose existing
* Existing security group = the security group you just created
Then scroll down and click the `Create database` button. After successful creation Click the `View credential details` button. You'll see your master username, master password, & endpoint. Keep track of these.

#### Test database
You can test it using code like this, from any Python notebook, shell, or script, in any environment (where sqlalchemy is installed). 
```
import sqlalchemy

# Replace username, password, & blah.blah.blah
database_url = 'postgresql://username:password@blah.blah.blah.us-east-1.rds.amazonaws.com/postgres'

engine = sqlalchemy.create_engine(database_url)
connection = engine.connect()
```
You know you’ve done it correctly if this code runs without error. 🎉





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







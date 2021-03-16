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

#### Create databas hosted in AWS
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

Don't share your passwords with the world. In your real app, use environment variables. When developing locally,  you can use python-dotenv to load a .env file. (The .env file is listed in .gitignore)  When you deploy, use the Elastic Beanstalk console for the [configuring environment variables](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html#environments-cfg-softwaresettings-console) there.

#### Test database
You can test it using code like this, from any Python notebook, shell, or script, in any environment (where sqlalchemy is installed). 
```
import sqlalchemy

# Replace username, password, & blah.blah.blah
database_url = 'postgresql://username:password@blah.blah.blah.us-east-1.rds.amazonaws.com/postgres'

engine = sqlalchemy.create_engine(database_url)
connection = engine.connect()
```
You know you’ve done it correctly if this code runs without error. 🎉 you can also connect by `pgadmin` or `datagrip`.

Or we can connect with psycopg2:
```python
import psycopg2

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

Let's see how to work with our database.
#### How to upload Data to DataBase
- Convert CSV/Excel into DataFrame format : 
```python 
df = pd.read("file_location")
```
- Upload DataFrame to SQL Table
```python   
con, c = conn_curs()
table_name = 'table_name'
df.to_sql(table_name, con)
```
- Test Queries to Table B2P_oct_2018
query  = """SELECT "Bridge_Name" from public."B2P_oct_2018" where "Bridge_Name" = 'Bukinga' LIMIT 1;"""
cursor.execute(query)
result = cursor.fetchall()
conn.close

### FastAPI app
Save your .env file in the following location: project/app/api/.env  and run the app locally from repo directory: `docker-compose up`, which will run `uvicorn app.main:app --reload` in the container. You can open it in browser at `localhost:80`.

#### example
An example for creating an endpoint:
open a new file: `app/messages.py`. Copy this starter code.
```
"""Friendly messsages"""
from fastapi import APIRouter
router = APIRouter()

@router.get('/hello')
async def hello():
    """Returns a friendly greeting 👋"""
    pass
```
Change the function so it returns JSON: `{"messsage": "Hello World!"}`
open the `app/main.py` file and import `messages` module.
```
from app import db, ml, viz, messages
```
and include the created route.
```
app.include_router(db.router, tags=['Database'])
app.include_router(ml.router, tags=['Machine Learning'])
app.include_router(viz.router, tags=['Visualization'])
app.include_router(messages.router, tags=['Friendly Messages'])
```
Refresh the browser now.
To change the function so it takes a person's name as input and returns messages like "Hello Alice!", Refer to the next sections in the FastAPI Tutorial:
* [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
* [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
* [Request Body](https://fastapi.tiangolo.com/tutorial/body/)
You can read about concurency and async keyword [here](https://fastapi.tiangolo.com/async/).

Links for more on FastAPI:
* [Build a machine learning API from scratch by FastAPI's creator](https://youtu.be/1zMQBe0l1bM)
* [calmcode.io — FastAPI videos](https://calmcode.io/fastapi/hello-world.html)
* [FastAPI for Flask Users](https://amitness.com/2020/06/fastapi-vs-flask/)
* [FastAPI official docs](https://fastapi.tiangolo.com/)
* [How to Set Up a HTML App with FastAPI, Jinja, Forms & Templates](https://eugeneyan.com/writing/how-to-set-up-html-app-with-fastapi-jinja-forms-templates/)
* [Implementing FastAPI Services – Abstraction and Separation of Concerns](https://camillovisini.com/article/abstracting-fastapi-services/)
* [testdriven.io — FastAPI blog posts](https://testdriven.io/blog/topics/fastapi/)

#### Deploy the FastAPI app to AWS Elastic Beanstalk
Follow these instructions to deploy the first time. 🚀

1. If you are not using docker and `Dockerfile` then you need to create a `Procfile`, with this line: `web: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker` (Like on Heroku, the Procfile tells AWS what command to run. We’ve had better luck in the past using gunicorn instead of uvicorn with the Python platform on AWS Elastic Beanstalk.)
2. install gunicorn
3. install typing-extensions (a dependency needed on Python 3.7, which is the version Elastic Beanstalk is still using)
4. build the docker image or pipenv install the above in an activated env
5. git add --all
6. git commit -m "Your commit message"
7. in pipenv: `eb init --platform python-3.7 --region us-east-1 CHOOSE-YOUR-NAME` (Instead of using `Docker` as the platform, use Python 3.7. AWS will look for either a `requirements.txt` or `Pipfile.lock` or `Pipfile` to install your dependencies, in that order. You should have both a `Pipfile.lock` and `Pipfile` in your repo.). If you are using docker image: `eb init --platform docker --region us-east-1 CHOOSE-YOUR-NAME`
8. eb create --region us-east-1 CHOOSE-YOUR-NAME
9. If your app uses environment variables, set them in the [Elastic Beanstalk console](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html#environments-cfg-softwaresettings-console)
10. eb open
11. Check your logs in the [Elastic Beanstalk console](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html), to see any error messages

Reference docs: 
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-apps.html
https://fastapi.tiangolo.com/deployment/manually/

#### Clean up AWS
If not needed delete all application versions and terminate the environment to avoid extra cost. Link to [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.Cleanup.html)

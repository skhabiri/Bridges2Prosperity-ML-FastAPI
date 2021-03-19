# Bridges to Prosperity
[Bridges to Prosperity (B2P)](https://www.bridgestoprosperity.org) footbridges works with isolated communities to create access to essential health care, education and economic opportunities by building footbridges over impassable rivers.

## Dataset
The main dataset is [B2P Dataset_2020.10.xlsx](https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/Data/B2P%20Dataset_2020.10.xlsx). It consists of survey data of 1472 sites (rows) with 44 features. The “Stage” column shows the status of the project. The “senior_engineering_review” shows if the site has been reviewed by engineering team or not. Among all the rows of the dataset only 65 projects are reviewed and approved and 24 projects are reviewed and rejected. The rest (1383 rows) do not have any target label. 

#### Data cleaning
[b2p_main_sk.ipynb](https://github.com/skhabiri/bridges-to-prosperity-b2p/blob/main/notebooks/b2p_main_sk.ipynb) is used to clean up the data to `df` dataframe and downloaded to [main_data_clean.csv](https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/notebooks/main_data_clean.csv). Additionally, a similar dataset [B2P_World_Dataset_2020.01.14.xls](https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/Data/B2P_World_Dataset_2020.01.14.xls) is loaded from https://data.world/ and merged with the main dataset in an attempt to extend the training data. 
```
def process_target(df):
  data = df.copy()

  # Split the dataset:
  # Positives:
  positive = (
      (data['senior_engineering_review_conducted']=='Yes') & 
      (data['bridge_opportunity_stage'].isin(
      ['Complete', 'Prospecting', 'Confirmed', 'Under Construction']))
      )
  
  # Negatives:
  negative = (
      (data['senior_engineering_review_conducted']=='Yes') & 
      (data['bridge_opportunity_stage'].isin(['Rejected', 'Cancelled']))
      )
  

  # Unknown:
  unknown = data['senior_engineering_review_conducted'].isna()

  print("We are assigning all these to unknow:")
  data['bridge_opportunity_stage'][data['senior_engineering_review_conducted'].isna()].value_counts()

  # Create a new column named "Good Site." This is the target to predict.
  # Assign a 1 for the positive class, 0 for the negative class and -1 for unkown class.
  data.loc[positive, 'good_site'] = 1
  data.loc[negative, 'good_site'] = 0
  data.loc[unknown, 'good_site'] = -1

  # Because these columns were used to derive the target, 
  # We can't use them as features, or it would be leakage.
  data = data.drop(columns=['senior_engineering_review_conducted', 'bridge_opportunity_stage'])
  print(data['good_site'].value_counts())
  
  return data
```
We selected 6 features that are most relevant to our target label and also convert the target label classes to 0,1, and -1, where 0 is rejected, 1 is accepted and -1 is for unknown.

## Project objective and challenge
As mentioned in Dataset section, a number of sites have been reviewed by the  senior engineering team and the projects have been either accepted or rejected to continue. Based on the existing input data we want to know if we can classify the sites as being rejected or not in any future review conducted by senior engineering team. In other words we want to find out which sites will be technically rejected in future engineering reviews.

Hene despite a very unbalance nature and number of samples we like to make a prediction on the engineering review final decision about the projects. We process the target label into three main classes as `Unknown`, `negative`, `positive`.
  ```python
  def process_target(df):
  data = df.copy()

  # Split the dataset:
  # Positives:
  positive = (
      (data['senior_engineering_review_conducted']=='Yes') & 
      (data['bridge_opportunity_stage'].isin(
      ['Complete', 'Prospecting', 'Confirmed', 'Under Construction']))
      )
  
  # Negatives:
  negative = (
      (data['senior_engineering_review_conducted']=='Yes') & 
      (data['bridge_opportunity_stage'].isin(['Rejected', 'Cancelled']))
      )
  

  # Unknown:
  unknown = data['senior_engineering_review_conducted'].isna()
```

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
## Virtual Environment:
We can either use `pipenv` or `docker` to reproduce the environment.

### pipenv
`cd` to the repo directory and install dependencies. In general `Pipfile` supercede `requirements.txt`. However, if you only have a `requirements.txt` file available when running `pipenv install --dev`, pipenv will automatically import the contents of this file and creates a `Pipfile` for you. You could also be specific with `pipenv install -r path/to/requirements.txt` to import a requirements file. 
Now activate the virtual environment with `pipenv shell`.
To work with the notebook you can create a ipykernel from the env and launch jupyter in env with `pipenv run jupyter lab`. In your VS Code IDE make sure you have the Python extension in **View → Extensions**, and activate the env by **View → Command Palette → Python: Select Interpreter**

In this project instead of pipenv we use Docker Compose to run our app in an isolated disposable container.

### Docker
For building a docker image we need Dockerfile which specifies: the base python to use, working directory on the image volume, all the package dependencies, and the files (web app) that needs to be copied from the host container to the image.
In this approach we build an image based on a python version and packagees specified in requirements.txt. We also map the local volume to the container volume that will be created based on this image. Additionally using docker-compose would allow us to run some services such as web server inside the container. For that we would need to define the networking ports, volume mapping and point of entry command to run.

## Architecture
The block diagram below shows different sections of the project.
<img src="https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/assets/b2p_diagram_update.png">

## File structure
```bash
bridges-to-prosperity-b2p
├── .ebignore
├── .elasticbeanstalk
│   └── config.yml
├── Data
│   ├── B2P\ Dataset_2020.10.xlsx
├── LICENSE
├── README.md
├── docker-compose.yml
├── notebooks
│   ├── Dockerfile
│   ├── README.md
│   ├── b2p_db_sk.ipynb
│   ├── b2p_main_sk.ipynb
│   ├── gs_model
│   ├── main_data_clean.csv
│   ├── predict_df.csv
│   └── requirements.txt
├── project
│   ├── .elasticbeanstalk
│   │   └── config.yml
│   ├── Dockerfile
│   ├── app
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── .env
│   │   │   ├── __init__.py
│   │   │   ├── dbpgsql.py
│   │   │   ├── gs_model
│   │   │   ├── predict.py
│   │   │   └── viz.py
│   │   ├── main.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── test_main.py
│   │       ├── test_predict.py
│   │       └── test_viz.py
│   └── requirements.txt
```

## AWS
AWS is a cloud platform that offers various services.

### Cloud Services
#### AWS EC2
`Amazon Elastic Compute Cloud` (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers. Amazon EC2’s simple web service interface allows you to obtain and configure capacity with minimal friction. This is like virtual private servers.

#### AWS Elastic Beanstalk
AWS Elastic Beanstalk is an easy-to-use service for deploying and scaling web applications and services developed with Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker on familiar servers such as Apache, Nginx, Passenger, and IIS.
You can upload your code and Elastic Beanstalk automatically handles the deployment, from capacity provisioning, load balancing, auto-scaling to application health monitoring. This is similar to Heroku.

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

#### AWS Route 53
Route 53 is Amazon's [Domain Name System (DNS)](https://simple.wikipedia.org/wiki/Domain_Name_System) web service, to set up the DNS records for a domain.

Follow the [instructions](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html#resource-record-sets-elb-dns-name-procedure) to configure a domain name with HTTPS for the DS API.

The way it works is, When a machine (or human) wants to connect to your API, they first need to find the IP address of the endpoint where your API is hosted.
This is step one, where the caller (aka client) asks the name servers in your hosted zone to translate your domain name (e.g. c-ds.ecosoap.dev) to a proper IP address.
Once the client has the IP address, it will connect to your API, which is hosted in your Elastic Beanstalk environment. We've made this connection secure by adding an SSL certificate to the load balancer and enabling HTTPS. The client will then send encrypted traffic over the internet to the loadbalancer attached to the API. Then, the load balancer sends the traffic to the actual API instances, running on servers or in containers. Since the load balancer and api application instance are on the same private network (not on the internet) we don't need to keep the traffic encrypted between them, which adds cost and reduces performance.
The traffic is decrypted by the load-balancer and sent to the application as unencrypted HTTP traffic on port 80.

<img src="https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/assets/SSL_aws.png" width="600" />

____
## Building The App
As a part of data science team the task is to train the model, deploy model in the cloud, and integrate machine learning into web product. The following tech stack is used:
* FastAPI: Web framework. Like Flask, but faster, with automatic interactive docs.
* AWS RDS Postgres: Relational database service. Like ElephantSQL.
* AWS Elastic Beanstalk: Platform as a service, hosts your API. Like Heroku.
* Docker: Containers, for reproducibility. Like virtual environments, but more reproducible.

### Setup AWS interface on the local host

#### Install AWS CLI (Command Line Interface):
Install the aws cli from [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html). Check that the aws cli is installed by `which aws`.

#### Install AWS Elastic Beanstalk CLI
Use `pip install awsebcli` for that and check the successful installation with `eb --version`. Later on we'll use that to deploy Docker image to AWS elastic beanstalk.

#### Sign into your aws account
Make sure to choose us-east-1 region, and create a IAM user for the app instead of using the root credentials. You would also want to take a note of the secret access key, access key id and the account id or create an account alias.

#### Configure AWS CLI
use `aws configure` to enter the credentials. Those data are saved in `~/.aws/credentials` and `~/.aws/config`.

#### Create security group
In EC2 service create a `security group`. This will be use when creating the database. In the `Inbound rules` section, click the `Add rule` button. For `Type`, select `PostgreSQL`. For `Source`, select `Anywhere`. Do the same for the Outbound.

### SQLAlchemy engine, connection, and session
**Engine** is the lowest level object used by SQLAlchemy. It [maintains a pool of connections](http://docs.sqlalchemy.org/en/latest/core/pooling.html) available for use whenever the application needs to talk to the database. .execute() is a convenience method that first calls `conn = engine.connect(close_with_result=True)` and then `conn.execute()`. The `close_with_result` parameter means the connection is closed automatically.

**Connection** is (as we saw above) the thing that actually does the work of executing a SQL query. You should do this whenever you want greater control over attributes of the connection, when it gets closed, etc. For example, a very import example of this is a Transaction, which lets you decide when to commit your changes to the database. In normal use, changes are autocommitted. With the use of transactions, you could (for example) run several different SQL statements and if something goes wrong with one of them you could undo all the changes at once.
```
connection = engine.connect()
trans = connection.begin()
try:
    connection.execute("INSERT INTO films VALUES ('Comedy', '82 minutes');")
    connection.execute("INSERT INTO datalog VALUES ('added a comedy');")
    trans.commit()
except:
    trans.rollback()
    raise
```
**Sessions** are used for the Object Relationship Management (ORM) aspect of SQLAlchemy (in fact you can see this from how they're imported: `from sqlalchemy.orm import sessionmaker)`. They use connections and transactions under the hood to run their automatically-generated SQL statements. `.execute()` is a convenience function that passes through to whatever the session is bound to (usually an engine, but can be a connection).
If you're using the ORM functionality, use session; if you're only doing straight SQL queries not bound to objects, you're probably better off using connections directly.

### AWS RDS Postgres
In order to have access to the dataset while connecting to data science API, We create a PostgreSQL database instance in Amazon RDS. Here you can find instruction for [creating a PostgreSQL DB Instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html#CHAP_GettingStarted.Creating.PostgreSQL).

#### Create databass hosted in AWS
Go to the RDS service. Click the `Create database` button. Select the following options:
* Database creation method = Standard create
* Engine type = PostgreSQL
* Template = Free tier
* DB instance identifier = mydbinst
* Master username = mypostgres
* Master password = you make up a password
Scroll down to the `Connectivity` section, and select the following options:
* Public access = Yes
* VPC security group = Choose existing
* Existing security group = the security group you just created
Then scroll down and click the `Create database` button. After successful creation Click the `View credential details` button. You'll see your master username, master password, & endpoint url. Keep track of these.

In your real app, use environment variables to hide the credentials from public. When developing locally,  you can use python-dotenv to load a .env file. (The .env file is listed in .gitignore)  When you deploy, use the Elastic Beanstalk console for the [configuring environment variables](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html#environments-cfg-softwaresettings-console) there.

#### Connect to AWS DB instance
After DB instance is created, you can use any standard SQL client application such as [pgAdmin](https://www.pgadmin.org/) to connect to the database instance. You can download and use pgAdmin without having a local instance of PostgreSQL on your client computer. `pgAdmin4` as a database client create a server connection to the RDS DB instance and we can use the pgAdmin gui to create multiple database in RDS DB Instance. 

We can connect to the created database from any Python notebook, shell, or script, in any environment (by `sqlalchemy` or `psycopg2`). 

Here is a snippet of the code in Jupyter Notebook.
```
# Install database related packages
!pip install python-dotenv
!pip install psycopg2-binary
!pip install SQLAlchemy
```
Add the newly installed packages to the requirements.txt file to rebuild docker-compose
```
echo python-dotenv >> requirements.txt
echo psycopg2-binary>> requirements.txt
echo SQLAlchemy>> requirements.txt
```
Import packages
```
import psycopg2
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import logging
```
Loading .env file with database credentials for local host
```
file_path = os.path.abspath('$APP_DIR')
load_dotenv(os.path.join(file_path, '.env'))

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
```
#### Connecting to the db by `sqlalchemy`:
In sqlalchemy we create an engine attached to the db and connect to it by:
```
# default PostgreSQL port is 5432
engine = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
con = engine.connect()
```
Create tables in the database and insert data into them. It's autocommit here.
```
dfp = pd.read_csv("../Data/predict_df.csv")
df = pd.read_csv("../Data/main_data_clean.csv")
df.to_sql('cleaneddata_table', con, if_exists='replace')
dfp.to_sql('model_table', con, if_exists='replace')
con.close()
```
*global variable in python:*
*Python assumes that any name that is assigned to, anywhere within a `function`, is `local` to that function unless explicitly told otherwise. If it is only **reading** from a name, and the name doesn't exist locally, it will try to look up the name in any containing scopes.*
```
# sample.py
myGlobal = 5

def func_loc():
    """ by default function variables are local"""
    myGlobal = "local_func"
    print(myGlobal)
    
def func_glob():
    """ by default function variables are local"""
    global myGlobal
    myGlobal = "global_func"

def func_read():
    print(myGlobal)

func_loc()  # prints: "local_func" and discards local variable upon exit
func_read() # prints: 5 as myGlobal is not found in local scope
func_glob() # updates myGlobal in global scope
func_read() # prints: "global_func" as myGlobal is not found in local scope
```
Let's make a query to validate the data

#### Connecting to the db by `psycopg2
```
def conn_curs():
    """
    makes a connection to the database
    """
    global db_name
    global db_user
    global db_password
    global db_host
    global db_port

    connection = psycopg2.connect(dbname=db_name, user= db_user, password=db_password, host= db_host,port=db_port)
    cursor = connection.cursor()
    return connection, cursor

def fetch_query_records(query):
    global conn_curs
    conn, cursor = conn_curs()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

fetch_query_records("""SELECT bridge_name from cleaneddata_table LIMIT 5;""")
```
Results:
[('Bukinga',),
 ('Kagarama',),
 ('Karambi',),
 ('Rugeti',),
 ('Nyakabuye - Nkomane',)]

you can also connect by `pgadmin` or `datagrip`.
The API gives us access to database for web development by providing JSON data.

### FastAPI app
An example on how to create an endpoint route for GET and POST requests.

#### GET request
open a new file: `app/messages.py`. Copy this starter code.
```
"""Friendly messsages"""
from fastapi import APIRouter
router = APIRouter()

@router.get('/hello')
async def hello():
  return {"messsage": "Hello World!"}
```
It returns JSON.

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

#### POST request
For example let's create a API endpoint for a machine learning model that predict rent. The input to the model is # of beds and baths. Then the endpoint should accept POST requests, not GET requests.
```
@router.post('/predict_rent')
async def rent(beds, baths):
  return {"rent": model.predict(beds, baths)}
```

Data science can deploy machine learning models through API endpoints. When clients make requests to your API endpoints, the inputs might not be valid. That means 
"Garbage in, garbage out". So we'll create a [data class](https://docs.python.org/3/library/dataclasses.html) with [type annotations](https://docs.python.org/3/library/typing.html) to define what attributes we expect our input to have. We'll use [Pydantic](https://pydantic-docs.helpmanual.io/), a data validation library integrated with FastAPI.
To learn more, see these docs:
* [Pydantic docs > Field types](https://pydantic-docs.helpmanual.io/usage/types/)
* [Pydantic docs > Validators](https://pydantic-docs.helpmanual.io/usage/validators/)

Links for more on FastAPI:
* [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
* [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
* [Request Body](https://fastapi.tiangolo.com/tutorial/body/)
You can read about concurency and async keyword [here](https://fastapi.tiangolo.com/async/).
* [Build a machine learning API from scratch by FastAPI's creator](https://youtu.be/1zMQBe0l1bM)
* [calmcode.io — FastAPI videos](https://calmcode.io/fastapi/hello-world.html)
* [FastAPI for Flask Users](https://amitness.com/2020/06/fastapi-vs-flask/)
* [FastAPI official docs](https://fastapi.tiangolo.com/)
* [How to Set Up a HTML App with FastAPI, Jinja, Forms & Templates](https://eugeneyan.com/writing/how-to-set-up-html-app-with-fastapi-jinja-forms-templates/)
* [Implementing FastAPI Services – Abstraction and Separation of Concerns](https://camillovisini.com/article/abstracting-fastapi-services/)
* [testdriven.io — FastAPI blog posts](https://testdriven.io/blog/topics/fastapi/)
* [FastAPI docs > Tutorial - User Guide > Request Body](https://fastapi.tiangolo.com/tutorial/body/)
* [FastAPI docs > Python Types Intro ](https://fastapi.tiangolo.com/python-types/)
* [FastAPI docs > Concurrency and async / await](https://fastapi.tiangolo.com/async/)
* [RealPython.com Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)

### Machine learning model
Looking at the target classes here is the distribution:
```
y.value_counts()
```
-1.0    1383
 1.0      65
 0.0      24
Name: good_site, dtype: int64
This is a semi-supervised learning as there are a large number of samples with no label. Additionally the labels are imbalanced and there is not sufficient rejected sites to build a reliable model. We use LabelSpreading and Synthetic Minority Oversampling Technique (SMOTE) to help with our imbalance dataset. Target classes are converted into 0 for negative, 1 for positive, and -1 as unknown. This type of assignment works better for label spreading technique.

Here is the pipeline estimator for the model:

```python
ss_model = make_pipeline_imb(
    ce.OneHotEncoder(use_cat_names=True, cols=nonnum_features),
    SimpleImputer(strategy='median'),
    StandardScaler(),
    SMOTE(random_state=42),
    LabelSpreading(kernel='knn', n_neighbors=2)
    )
```
In the absence of sufficient data, one of the challenges is how to evaluate the performance of the model. We can look at the confusion matrix to evaluate the number of mislabled data. We can also use cross validation technique to be able to use the validation data in training process as well.

Random forest classifier was also tried to be able to compare the models.
```python
pipe = make_pipeline_imb(
    ce.OneHotEncoder(use_cat_names=True, cols=nonnum_features),
    SimpleImputer(strategy='median'),
    StandardScaler(),
    SMOTE(random_state=42),
    RandomForestClassifier(n_estimators=100, random_state=42)
    )
```
We also did the hyper-parameter tunning and cross validation.
```
# Grid search CV for hypertunning and cross fold validation
""" This prediction problem cares more about precision than 
recall as it's more important to make a correct positive prediction
than getting all the positves"""

gs_params = {'randomforestclassifier__n_estimators': [100, 200, 50],
              'randomforestclassifier__max_depth': [4, 6, 10, 12], 
              'simpleimputer__strategy': ['mean', 'median']
}

gs_model = GridSearchCV(pipe, param_grid=gs_params, cv=10, 
                        scoring='precision',
                        return_train_score=True, verbose=0)
gs_model.fit(X_train, y_train)
```
The best estimator is saved for later evaluation. `gs_best = gs_model.best_estimator_`.

#### Model serialization
Now let's use a scikit-learn model. We want to save the a trained model so you can use it without retraining. This is sometimes called "pickling."  See [scikit-learn docs on "model persistence"](https://scikit-learn.org/stable/modules/model_persistence.html) & [Keras docs on "serialization and saving."](https://keras.io/guides/serialization_and_saving/)
```
import pickle
# Model serialization
pickle.dump(gs_best, open("gs_model", 'wb'))
model_gs = pickle.load(open("gs_model",'rb'))
```
#### Model prediction and evaluation
For training the model we selected six features that based on the domain knowlege seems to be most relevant to the engineering process review. After fitting the model we run some queries to evaluate the model accuracy. Here is the prediction function. It recieves a JSON data as input query for selected features and returns the predicted class as well as the probability of the prediction.
```
def prediction(model, query):
  """
  query is a JSON data for those 7 selected columns
  This is suitable for  our fastAPI
  """
  
  # query = pd.DataFrame(data=query, index=[0])
  query_ser = pd.DataFrame([dict(query)])
  # class prediction and its probability
  return model.predict(query_ser)[0], model.predict_proba(query_ser)[0][int(model.predict(query_ser)[0])]
```
Let's run some queries:
```
query = X_train.iloc[10,:].to_dict()
query
```
{'bridge_opportunity_bridge_type': 'Suspension Bridge',
 'bridge_opportunity_span_m': 85.0,
 'days_per_year_river_is_flooded': 121.0,
 'bridge_classification': 'Standard',
 'flag_for_rejection': 'No',
 'height_differential_between_banks': 0.97}
```
assert y[10] == prediction(model_gs, query)
prediction(model_gs, query)
```
(1.0, 0.9611480311321021)

With probability of 0.96 it predicts the target label is 1. In the process, I noticed that FastAPI treats the missing values of the selected features differently and the model can produce different results depending on how to fill the missing values.
Here is an example:
```
query2a = X_train.iloc[0,:].to_dict()
print(prediction(model_gs, query2a), y[0])
print(type(query2a['bridge_classification']))
print(query2a['bridge_classification'])
query2a
```
(0.0, 0.5231655566249169) 0.0
<class 'float'>
nan
{'bridge_opportunity_bridge_type': 'Suspended Bridge',
 'bridge_opportunity_span_m': 52.44,
 'days_per_year_river_is_flooded': 78.63,
 'bridge_classification': nan,
 'flag_for_rejection': 'Yes',
 'height_differential_between_banks': 0.97}

Now let's replace the missing value with different nan types:
```python
# Some inconsistancy issue with defining missing value types in FastAPI
query2b = {
  "bridge_classification": "",
  "bridge_opportunity_bridge_type": "Suspended Bridge",
  "bridge_opportunity_span_m": 52.44,
  "days_per_year_river_is_flooded": 78.63,
  "flag_for_rejection": "Yes",
  "height_differential_between_banks": 0.97 
}
print(query2b)
for val in ["nan","", None, np.nan]:
  query2b["bridge_classification"] = val
  print(type(query2b['bridge_classification']))
  print(prediction(model_gs, query2b))
```
{'bridge_classification': '', 'bridge_opportunity_bridge_type': 'Suspended Bridge', 'bridge_opportunity_span_m': 52.44, 'days_per_year_river_is_flooded': 78.63, 'flag_for_rejection': 'Yes', 'height_differential_between_banks': 0.97}

<class 'str'>
(1.0, 0.603189091907065)
<class 'str'>
(1.0, 0.603189091907065)
<class 'NoneType'>
(1.0, 0.603189091907065)
<class 'float'>
(1.0, 0.7013543055860129)

`"nan"`, `""`, `None` yield probability of 0.6, `np.nan` calculates the probability as 0.7 while missing value as was seen earlier resulted in probability of 0.52.

The cleaned up input data set is saved as [main_data_clean.csv](https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/notebooks/main_data_clean.csv). 
```
print(df.shape)
df.columns
```
(1472, 43)
Index(['bridge_name', 'bridge_opportunity_project_code',
       'bridge_opportunity_needs_assessment',
       'bridge_opportunity_level1_government',
       'bridge_opportunity_level2_government',
       'bridge_opportunity_gps_latitude', 'bridge_opportunity_gps_longitude',
       'bridge_opportunity_bridge_type', 'bridge_opportunity_span_m',
       'bridge_opportunity_individuals_directly_served',
       'bridge_opportunity_comments', 'form_form_name', 'form_created_by',
       'proposed_bridge_location_gps_latitude',
       'proposed_bridge_location_gps_longitude', 'current_crossing_method',
       'nearest_all_weather_crossing_point', 'days_per_year_river_is_flooded',
       'flood_duration_during_rainy_season', 'market_access_blocked_by_river',
       'education_access_blocked_by_river', 'health_access_blocked_by_river',
       'other_access_blocked_by_river', 'primary_occupations',
       'primary_crops_grown', 'river_crossing_deaths_in_last_3_years',
       'river_crossing_injuries_in_last_3_years', 'incident_descriptions',
       'notes_on_social_information', 'cell_service_quality',
       'four_wd _accessibility', 'name_of_nearest_city',
       'name_of_nearest_paved_or_sealed_road', 'bridge_classification',
       'flag_for_rejection', 'rejection_reason', 'bridge_type',
       'estimated_span_m', 'height_differential_between_banks',
       'bridge_opportunity_general_project_photos',
       'bridge_opportunity_casesafeid', 'country', 'good_site'],
      dtype='object')

The input train set for the model training is saved as [predict_df.csv](https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/notebooks/predict_df.csv).
```
print(X.shape)
X.columns
```
(1472, 7)
Index(['bridge_opportunity_bridge_type', 'bridge_opportunity_span_m',
       'days_per_year_river_is_flooded', 'bridge_classification',
       'flag_for_rejection', 'height_differential_between_banks'],
      dtype='object')

## Containerize the app in Docker-Compose
The essential proposition of a Docker container is we can develop and test the entire project on our local machine and set up everything that is needed to run it properly and when it's done we put the whole thing in a container and deploy it on the cloud being certain that it would behave the same way as on our local host. So there are two advantages or `portability` and `reproducibility`.

Docker-Compose is simply a tool that allows you to describe a collection of multiple containers that can interact via their own network. We compose the containers in docker-compose.yml. We define containers as services, define volumes to store data, set port forwards.
There are a few important concepts in docker that I would like to cover here.

#### Docker Engine
Docker engine is the layer on which Docker runs. It’s a lightweight runtime and tooling that manages containers, images, builds, and more. It runs natively on Linux systems and is made up of:
1. A Docker Daemon that runs in the host computer.
2. A Docker Client that communicates with the Docker Daemon through a REST API.

#### Docker Image
Images are read-only templates that you build from a set of instructions written in your Dockerfile. Images define both what you want your packaged application and its dependencies to look like *and* what processes to run when it’s launched.

The Docker image is built using a Dockerfile. Each instruction in the Dockerfile adds a new “layer” to the image,

#### Docker Containers
A Docker container, as discussed above, wraps an application’s software into an invisible box with everything the application needs to run. That includes the operating system, application code, runtime, system tools, system libraries, and etc. Docker containers are built off Docker images. Since images are read-only, Docker adds a read-write file system over the read-only file system of the image to create a container.

#### Union File Systems
Docker uses Union File Systems to build up an image. You can think of a Union File System as a stackable file system, meaning files and directories of separate file systems (known as branches) can be transparently overlaid to form a single file system. The images are read-only and the containers are writable.

<p align="middle">
  <img src="https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/assets/docker_layers.png" width="400" />
  <img src="https://github.com/skhabiri/bridges-to-prosperity-b2p/raw/main/assets/volumes_in_docker.png" width="400" /> 
</p>

#### Volumes
Volumes are the **data** part of a container, initialized when a container is created. Volumes allow you to persist and share a container’s data. Data volumes are separate from the default Union File System and exist as normal directories and files on the **host** filesystem. So, even if you destroy, update, or rebuild your container, the data volumes will remain untouched. When you want to update a volume, you make changes to it directly in the container. Basically when we run a container let's say for an app and generate some data, the data is going to be lost once we exit the docker environment. This is the property of the containers that are disposable. If we ever needed to persist the collected data, we could define a volume that would basically maps a local host directory to a path relative to working directory in the container. This would allow to directly write to the volume from the container and have the data persist even after we exit the container.
Additionally, data volumes can be shared and reused among multiple containers. That would be also helpful during building the images as we can decide what files to copy over to the container that would be built based on image and what files/data to share with a container without copying to the image.

In the docker-compose.yml we can use host:container format to define the volume mapping. The volume can be defined for each service or in a higher scope for all services in one place.
```
volumes:
  # Just specify a path in the container and let the Engine create a volume.
  # The location of the volume on the host can be retrieved by "docker volume inspect <ProjectDir>_<Named Volume>"
  - /var/lib/mysql

  # Specify an absolute path mapping
  - /opt/data:/var/lib/mysql

  # Path on the host, relative to the Compose file (docker-compose.yml)
  - ./cache:/tmp/cache

  # User-relative path
  - ~/configs:/etc/configs/:ro

  # Named volume
  - datavolume:/var/lib/mysql
```
The location of the `named volume` on the host can be retrieved by `docker volume inspect <ProjectDir>_<Named Volume>`.

#### Port forwarding
When creating the container, Docker creates a network interface so that the container can talk to the local host, attaches an available IP address to the container, and executes the process that we specified to run the application when defining the image. We can access a service port in a container by mapping it to a port in the local docker host: `host_port:container_port`.

#### Dockerfile
A Dockerfile is where you write the instructions to build a Docker image. RUN is an image build step, the state of the container after a RUN command will be committed to the container image. A Dockerfile can have many RUN steps that layer on top of one another to build the image.

This Dockerfile is used to create "apiwebapp" service image, which is defined in docker-compose.yml
```
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
```

This Dockerfile is used to create "ipynotebook" service image, which is defined in "docker-compose.yml"
```
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
#COPY . .
#COPY ../Data/ /usr/src/b2p/Data/

```

Compose file allows to define multiple services each with potentially a separate build and docker file and hence defferent container. This is done by dockerp-compose.yml.

#### docker-compose.yml
We use docker-compose.yml to define the services, entry point command, volume and network port mapping from the docker host to the container. We can define dependency of the services to eachother or in other word the sequence of the services to start up. With `command` We can overwrite the CMD in dockerfiles and define what each service does when starts up. We can designate separate docker file to each service and specifiy its location for building a service image. 
CMD is the command the container executes by default when we launch the built image. A Dockerfile will only use the final CMD defined. The CMD can be overridden when starting a container with docker run $image $other_command.

Here we have two services. One for the web app named `apiwebapp` and the other one named `ipynotebook` is used to launch a teminal and start a jupyter kernel to edit the notebook files. `ipynotebook` service uses `apiwebapp` service image as the base. Hence inherits all the installed packages.
Another way to execute a command such as jupyuter kernel server in a running container is to 
1. `docker-compose up`
2. switchto another terminal and open a bash associated with a service container
  - `docker-compose exec ipynotebook /bin/bash`
3. Run any command in the container bash session
  - `jupyter lab --debug --ip='*' --allow-root`


```
# Each service can be built separately and would have its own image and container

version: '3.7'


services:
    
    # service name is arbitrary
    apiwebapp:
        
        # tag a name to its docker built image
        image: b2p/fastapi-app
        
        # The apiwebapp service builds an image with a Dockerfile located in the ./project directory.
        build: 
            context: ./project
        
        # Command to run, when docker container is created, `docker-compose up`
        command: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
    
        # mounts volume ./project to container's /usr/src/app path
        #volumes:
        #    - ./project:/usr/src/app
    
        
        # maps container port 8000 to TCP port 80 on the docker host and from there to the outside world
        ports:
            - 80:8000

    
    ipynotebook:
    
        image: b2p/notebook
        
        stdin_open: true
        tty: true
        
        # The web service uses an image that’s built from the Dockerfile located in the ./notebooks directory.
        build: 
            context: ./notebooks
    
        # First starts the apiwebapp and then ipynotebook.
        # Not really needed here
        depends_on:
            - apiwebapp
        
        # Jupiter lab runs on port 8888 of the docker image "b2p/notebook"   
        # bash -c allows multiple command
                
        command: bash -c "jupyter lab --debug --ip='*' --port=8888 --allow-root && /bin/bash"
        
        # alternative way to launch shell for a service container. 
        # Enter `docker-compose up`, then open another terminal
        # 1. docker-compose exec ipynotebook /bin/bash # use `exit` to exit the service shell
        # Now we can launch jupyter in the docker container that belongs to the service
        # 2. jupyter lab --debug --ip='*' --allow-root 
    
        volumes:
            - ./Data:/usr/src/b2p/Data
            - ./notebooks:/usr/src/b2p/notebooks
        
        # maps local host port 8888 to docker image ("b2p/notebook") port 8888
        ports:
            - 8888:8888
            - 8889:8889
```

mounting ./project directory on the host to /use/src/app inside the container, allows modifying the code on the fly, without having to rebuild the image, as the container gets updated in real time.
In docker-compose.yml we have 80:8000 on the last line. This will connect host port 80 (the default port for HTTP) to container port 8000 (where the app is running).

#### Build and run the docker-compose

From the directory with docker-compose.yml we build the docker service images:
```
docker-compose build #builds the images, does not start the containers
docker-compose up #builds the images if the images do not exist and starts the container
docker-compose up --build #forced to build the images even when not needed and starts the containers
```
To list the images used to create containers, use `docker-compose images`, or `docker images`. With defining the volumes you won't need to rebuild when you update your code. You'll only need to rebuild if you update your requirements.txt or Dockerfile.

## Run the app on the local host
Save your .env file in the following location: project/app/api/.env  and run the app locally from repo directory where docker-compose.yml exist: `docker-compose up`, which will run `uvicorn app.main:app --reload` in the container with specified python version in the base image, `python:3.8-slim-buster` and installed packages built in the docker images. 

You can open the `apiwebapp` service  in a browser at `localhost:80` (http://0.0.0.0:80).
Or if using pipenv instead of docker-compose:
```
pipenv shell
uvicorn app.main:app --reload
```
docker-compose specification can be found [here](https://github.com/compose-spec/compose-spec).

## Deploy the FastAPI app to AWS Elastic Beanstalk
Follow these instructions to deploy the first time. 🚀

1. If you are not using docker and `Dockerfile` then you need to create a `Procfile`, with this line: `web: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker` (Like on Heroku, the Procfile tells AWS what command to run. We’ve had better luck in the past using gunicorn instead of uvicorn with the Python platform on AWS Elastic Beanstalk.). If you are using docker platform, Dockerfile is sufficient to build the image and launch it in beanstalk.
2. install gunicorn
3. install typing-extensions (a dependency needed on Python 3.7, which is the version Elastic Beanstalk is still using)
4. build the docker image or pipenv install the above in an activated env
5. `git add --all`
6. `git commit -m "Your commit message"`
7. `eb init --platform docker your-app-name --region us-east-1`
  - in pipenv: `eb init --platform python-3.7 --region us-east-1 CHOOSE-YOUR-NAME` (Instead of using `docker` as the platform, use Python 3.7. AWS will look for either a `requirements.txt` or `Pipfile.lock` or `Pipfile` to install your dependencies, in that order. You should have both a `Pipfile.lock` and `Pipfile` in your repo.). 
8. `eb create your-app-name`
9. If your app uses environment variables, set them in the [Elastic Beanstalk console](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html#environments-cfg-softwaresettings-console)
10. `eb open`
11. Check your logs in the [Elastic Beanstalk console](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html), to see any error messages. When your application is deployed to Elastic Beanstalk, you'll get an automatically generated URL that you can use to connect to your API.

Reference docs: 
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-apps.html
https://fastapi.tiangolo.com/deployment/manually/

#### Packages
Here are the list of packages used
Package             Version
------------------- ---------
anyio               2.2.0
argon2-cffi         20.1.0
async-generator     1.10
attrs               20.3.0
Babel               2.9.0
backcall            0.2.0
bleach              3.3.0
category-encoders   2.2.2
certifi             2020.12.5
cffi                1.14.5
chardet             4.0.0
click               7.1.2
cycler              0.10.0
decorator           4.4.2
defusedxml          0.7.1
entrypoints         0.3
et-xmlfile          1.0.1
fastapi             0.60.1
greenlet            1.0.0
h11                 0.9.0
httptools           0.1.1
idna                2.10
imbalanced-learn    0.4.3
imblearn            0.0
ipykernel           5.5.0
ipython             7.21.0
ipython-genutils    0.2.0
jedi                0.18.0
Jinja2              2.11.3
joblib              1.0.1
json5               0.9.5
jsonschema          3.2.0
jupyter-client      6.1.12
jupyter-core        4.7.1
jupyter-packaging   0.7.12
jupyter-server      1.4.1
jupyterlab          3.0.11
jupyterlab-pygments 0.1.2
jupyterlab-server   2.3.0
kiwisolver          1.3.1
MarkupSafe          1.1.1
matplotlib          3.3.4
mistune             0.8.4
nbclassic           0.2.6
nbclient            0.5.3
nbconvert           6.0.7
nbformat            5.1.2
nest-asyncio        1.5.1
notebook            6.2.0
numpy               1.20.1
openpyxl            3.0.7
packaging           20.9
pandas              1.2.3
pandocfilters       1.4.3
parso               0.8.1
patsy               0.5.1
pexpect             4.8.0
pickleshare         0.7.5
Pillow              8.1.2
pip                 21.0.1
plotly              4.9.0
prometheus-client   0.9.0
prompt-toolkit      3.0.17
psycopg2-binary     2.8.6
ptyprocess          0.7.0
pycparser           2.20
pydantic            1.8.1
Pygments            2.8.1
pyparsing           2.4.7
pyrsistent          0.17.3
python-dateutil     2.8.1
python-dotenv       0.14.0
pytz                2021.1
pyzmq               22.0.3
requests            2.25.1
retrying            1.3.3
scikit-learn        0.22
scipy               1.6.1
seaborn             0.11.0
Send2Trash          1.5.0
setuptools          54.1.1
six                 1.15.0
sniffio             1.2.0
SQLAlchemy          1.4.1
starlette           0.13.6
statsmodels         0.12.2
terminado           0.9.3
testpath            0.4.4
tornado             6.1
traitlets           5.0.5
typing-extensions   3.7.4.3
urllib3             1.26.4
uvicorn             0.11.8
uvloop              0.15.2
wcwidth             0.2.5
webencodings        0.5.1
websockets          8.1
wheel               0.36.2
xlrd                2.0.1





## Clean up AWS
If not needed delete all application versions and terminate the environment to avoid extra cost. Link to [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.Cleanup.html)

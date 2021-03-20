from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import predict, dbpgsql
app = FastAPI(
    title='Bridges To Prosperity - FastAPI app',
    description="### A data Science API utilizing FastAPI framework to deploy a machine learning model for development of a full stack web app.""",
    version='0.3',
    docs_url='/',
)


app.include_router(dbpgsql.router)
app.include_router(predict.router)
# app.include_router(viz.router)


@app.get('/')
def docs():
    """
    [Github Repo:](https://github.com/skhabiri/Bridges2Prosperity-ML-FastAPI)
    *********************************
    This Data Science API uses FastAPI framework to deploy
    a machine learning model for development of a full stack web app. The
    predictive model is a classifier. It takes seven input feature for a
    surveyed bridge project and returns a prediction with its corresponding 
    probability of the project being rejected; 0; or approved; 1.
    
    The main dataset containing all the surveyed data is stored under the 
    table name `cleaneddata_table` in an AWS RDS database. A subset of it, 
    which is used to train the model and contains 7 selected features is stored
    under the table name `model_table`.
    
    The data science api provides four routes:
    1. **/data_by_bridge_code**
        - It's a post method. The user enters the `project_code` and the 
        `tablename`. The API connects to the corresponding table and fetches
        the queried record. Bothe request and response bodies are in JSON format.
    2. **/all_data**
        - fetch all the data from `cleaneddata_table`. Note that depending on 
        the number of the records in dastabase this might take a while.
    3. **/prediction**
        - This route connects to machine learning model. The request body is a
        JSON format of the seven selected features with their values used in 
        the model and the response body is the predicted class; 0 for negative 
        and 1 for positive with the probability of the prediction.
    4. **/**
        - root route provides documentation and url link to github repository.
    """
    return

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)

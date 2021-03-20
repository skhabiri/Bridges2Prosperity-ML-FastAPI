from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import predict, dbpgsql
app = FastAPI(
    title='Bridges To Prosperity - FastAPI app',
    description='# Version3-Deployment',
    version='0.3',
    docs_url='/',
)


app.include_router(dbpgsql.router)
app.include_router(predict.router)
# app.include_router(viz.router)


@app.get('/')
def github_repo():
    """
    https://github.com/skhabiri/Bridges2Prosperity-ML-FastAPI
    
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

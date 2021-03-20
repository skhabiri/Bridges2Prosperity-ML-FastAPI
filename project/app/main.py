from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# from app.api import predict, viz, database
from app.api import predict, viz, dbpgsql

app = FastAPI(
    title='Bridges To Prosperity- FastAPI app',
    description='# Version3-Deployment',
    version='0.3',
    docs_url='/',
)

app.include_router(dbpgsql.router)

app.include_router(predict.router)
# app.include_router(viz.router)

@router.get('/')
async def root():
    """
    Documentation
    """
    docs1 = ""
    return https://raw.githubusercontent.com/skhabiri/Bridges2Prosperity-ML-FastAPI/main/README.md

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)

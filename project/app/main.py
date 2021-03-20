from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import APIRouter


from app.api import predict, dbpgsql
app = FastAPI(
    title='Bridges To Prosperity - FastAPI app',
    description='# Version3-Deployment',
    version='0.3',
    docs_url='/',
)

router = APIRouter()

app.include_router(dbpgsql.router)
app.include_router(router)
app.include_router(predict.router)
# app.include_router(viz.router)


@router.get('/docs')
async def documents():
    """
    Documentation
    """
    url = "https://raw.githubusercontent.com/skhabiri/Bridges2Prosperity-ML-FastAPI/main/README.md"
    with open(url, "r") as file:
        doc = file.read()
    print("im in root")
    return "testinggggggggggggggggggg"

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)

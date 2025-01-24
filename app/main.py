from fastapi import FastAPI
import os
from dotenv import load_dotenv
from app.routers import router
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials


from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
app = FastAPI(docs_url=None, redoc_url=None, openapi_url = None)
app.include_router(router)

origins = ["*"]



security = HTTPBasic()

@app.get("/")
def read_root():
    return JSONResponse(content={"message":"OK"} ,status_code=200)

@app.post("/")
def read_root2():
    return JSONResponse(content={"message":"POST OK 2"} ,status_code=200)


app.add_middleware(
    CORSMiddleware,    
    allow_origins=origins,    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

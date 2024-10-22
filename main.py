from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

test = os.getenv('test')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
            "SUPABASE_URL": SUPABASE_URL
        }
    )


@app.get("/test")
async def read_test(request: Request):
    return JSONResponse(content={
        "Hello": "World",
        "SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
        "SUPABASE_URL": SUPABASE_URL
    })


@app.get("/create-account", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="create-account.html")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


@app.get("/test/{path}",
         name="Test Page",
         description="This is the test page",
         response_model=dict
         )
async def home(path: str):
    return JSONResponse(content={
        "message": path,
        "env_test": test
    })

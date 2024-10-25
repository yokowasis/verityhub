from cgitb import handler
import json
from typing import Dict
from fastapi import FastAPI, Body, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from modules.fn import db
from supabase import create_client, Client
import os

from modules.fn import getAllPosts

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


class CookieData(BaseModel):
    key: str
    value: str


_1week = 6134400


class LoginData(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(data: LoginData, response: Response):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    anon: Client = create_client(url, key)

    try:
        p = anon.auth.sign_in_with_password(credentials={
            "email": data.username + "@verityhub.id",
            "password": data.password
        })

        rows = db.table("users").select("handler, full_name, avatar").eq(
            "user_id", p.user.id).execute()

        data = rows.data[0]

        response.set_cookie(key="data", value=json.dumps(data),
                            max_age=_1week, httponly=True)
        return {"message": "Login Success !"}

    except:
        response.delete_cookie(key="id")
        return {"message": "Login Failed !"}


@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="data")
    return {"message": "Logout Success !"}


class UserData(BaseModel):
    handler: str
    full_name: str
    avatar: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    posts = getAllPosts()
    cookie = request.cookies.get("data")

    data = UserData(handler="", full_name="", avatar="")

    if (cookie):
        data = UserData(**json.loads(cookie))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "handler": data.handler,
            "full_name": data.full_name,
            "avatar": data.avatar,
            "ALL_POSTS": posts,
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

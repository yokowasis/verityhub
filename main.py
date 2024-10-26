import json
from fastapi import Cookie, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from modules.fn import getAllPosts, semanticSearch
from modules.auth import login, signup

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


@app.get("/test")
async def test(data: str = Cookie(None)):
    return data


class LoginData(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login_user(data: LoginData, response: Response, request: Request):
    data = login(username=data.username, password=data.password)
    if (data['data']):
        response.set_cookie(key="data", value=json.dumps(
            data['data']), max_age=_1week, httponly=True)
        return data
    else:
        response.delete_cookie(key="data")
        return {"message": "Login Failed !"}


class SignupData(BaseModel):
    username: str
    password: str
    avatar: str
    full_name: str


@app.post("/signup")
async def signup_user(data: SignupData, response: Response):
    username = data.username
    password = data.password
    avatar = data.avatar
    full_name = data.full_name

    try:
        res = signup(username, password, avatar, full_name)
        return res
    except Exception as e:
        print(e)
        return {"message": "Signup Failed !"}


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
        cookie_json = json.loads(cookie)
        data = UserData(
            avatar=cookie_json['avatar'], full_name=cookie_json['full_name'], handler=cookie_json['username'])

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "handler": data.handler,
            "full_name": data.full_name,
            "avatar": data.avatar,
            "ALL_POSTS": posts,
        }
    )


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

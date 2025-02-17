import datetime
import json
import os
from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from sympy import content
from modules.ai_model import encodeEmbedding, getSemanticSearchResult, semanticSearch, summarize
from modules.fn import doQuery, getAllPosts
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


class CookieData(BaseModel):
    key: str
    value: str


_1week = 6134400


@app.get("/test")
async def test():
    rows = semanticSearch("Hello World", 10)

    return rows


class LoginData(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login_user(data: LoginData, response: Response, request: Request):
    login_data = login(username=data.username, password=data.password)
    if (login_data['data']):
        response.set_cookie(key="data", value=json.dumps(
            login_data['data']), max_age=_1week, httponly=True)
        return login_data
    else:
        response.delete_cookie(key="data")
        return {"message": "Login Failed !"}


@app.get("/signin", response_class=HTMLResponse)
async def signin(request: Request):
    return templates.TemplateResponse(request=request, name="signin.html")


@app.get("/signup", response_class=HTMLResponse)
async def signupget(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")


class PostData(BaseModel):
    content: str
    parent: str
    posttype: str


@app.post("/post")
async def post(data: PostData, response: Response, request: Request):
    content = data.content
    posttype = data.posttype
    parent = data.parent

    if (not posttype):
        posttype = "post"

    if (not parent):
        parent = None

    summary = summarize(content)
    vector = encodeEmbedding(summary)
    cookie = request.cookies.get("data")
    if (cookie):
        data_json = json.loads(cookie)
        user_data = UserData(
            avatar=data_json['avatar'], full_name=data_json['full_name'], handler=data_json['username'])

        sql = "INSERT INTO posts (content,content_vec,summary,username,type,parent) VALUES (%s,%s,%s,%s,%s,%s);"
        params = (content,  vector, summary,
                  user_data.handler, posttype, parent)
        r = doQuery(sql, params)
        if (r):
            return {
                "message": "Post Success !",
                "data": data_json
            }
        else:
            return {"message": "Post Failed !"}

    else:
        return {"message": "Not Authorized !"}


class PostArticleData(BaseModel):
    content: str
    title: str


@app.post("/post-article")
async def postarticle(data: PostArticleData, response: Response, request: Request):
    content = data.content
    posttype = "article"
    parent = None
    title = data.title

    summary = summarize(content)
    vector = encodeEmbedding(summary)
    cookie = request.cookies.get("data")
    if (cookie):
        data_json = json.loads(cookie)
        user_data = UserData(
            avatar=data_json['avatar'], full_name=data_json['full_name'], handler=data_json['username'])

        sql = "INSERT INTO posts (content,content_vec,summary,username,type,parent,title) VALUES (%s,%s,%s,%s,%s,%s,%s);"
        params = (content,  vector, summary,
                  user_data.handler, posttype, parent, title)
        r = doQuery(sql, params)
        if (r):
            return {
                "message": "Post Success !",
                "data": data_json
            }
        else:
            return {"message": "Post Failed !"}

    else:
        return {"message": "Not Authorized !"}


@app.get("/articles")
async def getArticles(request: Request):
    posts = getAllPosts("article")

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
    cover: str | None = None
    bio: str | None = None
    link: str | None = None


@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request: Request):

    cookie = request.cookies.get("data")

    data = UserData(handler="", full_name="", avatar="", cover="", link="")

    if (cookie):
        cookie_json = json.loads(cookie)
        data = UserData(
            avatar=cookie_json['avatar'],
            full_name=cookie_json['full_name'],
            handler=cookie_json['username'],
            cover=cookie_json['cover'],
            bio=cookie_json['bio'],
            link=cookie_json['link'])

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "request": request,
            "handler": data.handler,
            "full_name": data.full_name,
            "avatar": data.avatar,
            "profile_cover": data.cover,
            "profile_bio": data.bio,
            "profile_link": data.link
        }
    )


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    posts = getAllPosts("post")

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


@app.get("/search", response_class=HTMLResponse)
async def searchRoute(
    request: Request,
    q: str = Query(..., description="Search Query"),
    limit: int = Query(10, description="Limit of Results"),
    page: int = Query(1, description="Page Number")
):

    posts = getSemanticSearchResult(q)
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
async def create_account(request: Request):
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

# handle upload
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'}

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# mount upload directory
app.mount("/api/files/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/edit-profile")
async def edit_profile(request: Request):

    data = request.cookies.get("data")
    if (data):
        data = json.loads(data)
        data = UserData(
            handler=data['username'],
            full_name=data['full_name'],
            avatar=data['avatar']
        )
        return templates.TemplateResponse(
            request=request,
            name="edit-profile.html",
            context={
                "request": request,
                "handler": data.handler,
                "full_name": data.full_name,
                "avatar": data.avatar,
            }
        )

        return templates.TemplateResponse(request=request, name="edit-profile.html")
    else:
        return templates.TemplateResponse(request=request, name="404.html")


@app.post("/api/files/")
async def upload_file(request: Request, filekey: str):
    try:
        # Read the binary content from the request body
        binary_content = await request.body()

        # Define the file path
        file_path = os.path.join(UPLOAD_DIR, filekey)

        # Get the file extension
        file_extension = os.path.splitext(filekey)[1][1:].lower()

        # Check if the file extension is allowed
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid file type.")

        # Save the binary content to the file
        with open(file_path, "wb") as file:
            file.write(binary_content)

        # Output a success message
        return JSONResponse(content={"message": "File uploaded successfully.", "file": filekey})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/new-article", response_class=HTMLResponse)
async def read_new_article(request: Request):

    posts = getAllPosts("post")

    cookie = request.cookies.get("data")

    data = UserData(handler="", full_name="", avatar="")

    if (cookie):
        cookie_json = json.loads(cookie)
        data = UserData(
            avatar=cookie_json['avatar'], full_name=cookie_json['full_name'], handler=cookie_json['username'])

    return templates.TemplateResponse(
        request=request,
        name="new-article.html",
        context={
            "request": request,
            "handler": data.handler,
            "full_name": data.full_name,
            "avatar": data.avatar,
            "ALL_POSTS": posts,
        }
    )


class PostResult(BaseModel):
    id: int
    created_at: datetime.datetime
    content: str
    content_vec: str | None
    content_ts: str | None
    summary: str | None
    username: str
    type: str
    parent: int | None
    title: str | None


@app.get("/generate-vector")
async def generate_vector(request: Request):
    """
    Generate Vector for all posts
    """

    rows = doQuery("SELECT * FROM posts WHERE content_vec IS NULL;")

    if (not rows or rows == True):
        return {"message": "No posts to generate vector"}

    for row in rows:

        data = PostResult(**vars(row))

        summary = summarize(data.content)
        vector = encodeEmbedding(summary)

        # update content_vec and summary
        doQuery("UPDATE posts SET content_vec = %s, summary = %s WHERE id = %s;",
                (vector, summary, data.id))

    return {"message": "Success"}

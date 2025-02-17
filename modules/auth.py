import bcrypt
import jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from modules.fn import doQuery

load_dotenv()

POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
SALT = os.getenv("SALT")


class authModel(BaseModel):
    username: str
    role: str
    full_name: str
    avatar: str
    cover: str
    bio: str
    link: str


def login(username: str, password: str):

    hashed_password = hash_password(password)

    sql = "SELECT username,role,full_name,avatar,cover,bio,link FROM users_auth WHERE username = %s AND password = %s"
    params = (username, hashed_password)
    rows = doQuery(sql, params)

    if (type(rows) == list):
        if len(rows):

            row = authModel(**vars(rows[0]))

            data = {
                "username": row.username,
                "role": row.role,
                "full_name": row.full_name,
                "avatar": row.avatar,
                "cover": row.cover,
                "bio": row.bio,
                "link": row.link,
            }

            return {
                "data": data,
                "message": "Login Success !",
            }

        else:
            return {"message": "Login Failed !", "data": None}

    else:
        return {"message": "Login Failed !", "data": None}


def hash_password(password: str):
    # Generate a salt and hash the password
    # bcrypt.gensalt()
    if (SALT):
        salt = SALT.encode('utf-8')
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    else:
        return password


def signup(username: str, password: str, avatar: str, fullname: str):

    # check if user already exists
    sql = "SELECT username FROM users_auth WHERE username = %s"
    selectParams = (username,)
    rows = doQuery(sql, selectParams)

    if (type(rows) == list):
        if len(rows):
            return {"message": "User Already Exists !"}

    hashed_password = hash_password(password)

    sql = "INSERT INTO \"users_auth\" (username, password, full_name, avatar, role) VALUES (%s, %s, %s, %s, 'user');"
    insertParams = (username, hashed_password, fullname, avatar)
    doQuery(sql, insertParams)
    return {"message": "Signup Success !"}

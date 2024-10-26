import bcrypt
import jwt
import os
from dotenv import load_dotenv
from modules.fn import doQuery

load_dotenv()

POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
JWT_SECRET = os.getenv("JWT_SECRET")
SALT = os.getenv("SALT")


def verifyjwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except:
        return None


def login(username: str, password: str):

    hashed_password = hash_password(password)

    sql = "SELECT username,role,full_name,avatar FROM users_auth WHERE username = %s AND password = %s"
    params = (username, hashed_password)
    rows = doQuery(sql, params)

    if rows:
        row = rows[0]
        data = {
            "username": row.username,
            "role": row.role,
            "full_name": row.full_name,
            "avatar": row.avatar
        }
        token = jwt.encode(data, JWT_SECRET, algorithm="HS256")

        return {
            "message": "Login Success !",
            "token": token,
            "data": data
        }

    else:
        return {"message": "Login Failed !", "data": None}


def hash_password(password: str):
    # Generate a salt and hash the password
    # bcrypt.gensalt()
    salt = SALT.encode('utf-8')
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def signup(username: str, password: str, avatar: str, fullname: str):

    # check if user already exists
    sql = "SELECT username FROM users_auth WHERE username = %s"
    params = (username,)
    rows = doQuery(sql, params)

    if len(rows):
        return {"message": "User Already Exists !"}

    hashed_password = hash_password(password)

    sql = "INSERT INTO \"users_auth\" (username, password, full_name, avatar, role) VALUES (%s, %s, %s, %s, 'user');"
    params = (username, hashed_password, fullname, avatar)
    doQuery(sql, params)
    return {"message": "Signup Success !"}

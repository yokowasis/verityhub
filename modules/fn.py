import http
import http.client
import json
import os
from typing import List
import urllib.parse
from dotenv import load_dotenv
import psycopg2
import psycopg2.pool
import urllib

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

# Database configuration
DATABASE_CONFIG = {
    "dbname": os.getenv("POSTGRES_DATABASE"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOSTNAME"),
    "port": os.getenv("POSTGRES_PORT"),
}


def get_connection():
    try:
        # Get a connection from the pool
        connection = connection_pool.getconn()
        return connection
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None


def release_connection(connection):
    try:
        # Release the connection back to the pool
        if connection:
            connection_pool.putconn(connection)
    except Exception as e:
        print(f"Error releasing connection back to pool: {e}")


# Initialize the connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,  # Minimum number of connections
    maxconn=10,  # Maximum number of connections
    **DATABASE_CONFIG
)


class SQLRecord:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def doQuery(sql, params=None):
    """
    Executes an SQL query with the provided parameters and returns results as instances of Record class.

    Parameters:
        sql (str): The SQL query to execute.
        params (tuple): Optional tuple of parameters to pass with the query.

    Returns:
        list: Query results as a list of Record instances.

    Example for a SELECT query:
    ```
    select_sql = "SELECT * FROM orders WHERE user = %s;"
    select_params = ('verityhub',)
    rows = doQuery(select_sql, select_params)
    for row in rows:
        print(row.id, row.user)
    ```

    Example for an INSERT query:
    ```
    insert_sql = "INSERT INTO orders (user, barang) VALUES (%s, %s);"
    insert_params = ('verityhub', 'Keyboard')
    doQuery(insert_sql, insert_params)
    ```
    """
    connection = get_connection()
    if not connection:
        print("Unable to get connection from the pool.")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            # Fetch results for SELECT queries
            if cursor.description:  # Checks if query returns results
                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [SQLRecord(**dict(zip(column_names, row))) for row in rows]
            # Commit transaction for INSERT, UPDATE, DELETE
            connection.commit()
            return True  # Non-SELECT queries don't return rows

    except Exception as e:
        print(f"Query failed: {e}")
        connection.rollback()  # Rollback transaction on failure
        return None

    finally:
        release_connection(connection)


def getVector(text: str):
    connection = http.client.HTTPSConnection(
        "nlp.backend.b.app.web.id")
    connection.request(
        "POST",
        "/api/vectorize",
        headers={
            "Content-Type": "application/json",
        },
        body=json.dumps({
            "text": text,
        }),
    )
    response = connection.getresponse()
    # print(response.status, response.reason)
    rows = response.read().decode()
    connection.close()
    s: List[int] = json.loads(rows)
    return s


def getSummary(text: str):
    connection = http.client.HTTPSConnection(
        "nlp.backend.b.app.web.id")
    connection.request(
        "POST",
        "/api/summarize",
        headers={
            "Content-Type": "application/json",
        },
        body=json.dumps({
            "text": text,
        }),
    )
    response = connection.getresponse()
    # print(response.status, response.reason)
    rows = response.read().decode()
    connection.close()
    s: str = json.loads(rows)
    return s


def semanticSearch(text: str):
    connection = http.client.HTTPSConnection(
        "supabase-api.b.app.web.id")
    connection.request(
        "GET",
        "/functions/v1/search-posts?text=" + urllib.parse.quote(text),
        headers={
            "Content-Type": "application/json",
        }
    )
    response = connection.getresponse()
    # print(response.status, response.reason)
    rows = response.read().decode()
    connection.close()
    return json.loads(rows)


def getAllPosts():

    sql = "SELECT posts.content, users_auth.full_name, users_auth.username, users_auth.avatar FROM posts JOIN users_auth ON posts.username = users_auth.username ORDER BY posts.created_at DESC LIMIT 10;"

    rows = doQuery(sql, ())

    html = ""

    for row in rows:
        html += f"""
          <div class="post">
            <v-profile
            fullname="{row.full_name}" 
            handler="{row.username}"
            avatar="{row.avatar}"
            ></v-profile>
            <div class="content">
              {row.content}
            </div>
          </div>
          """

    return html

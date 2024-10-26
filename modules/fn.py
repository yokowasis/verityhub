import http
import http.client
import json
import os
import urllib.parse
from dotenv import load_dotenv
import psycopg2
import psycopg2.pool
from supabase import create_client, Client
import urllib
import bcrypt

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
db: Client = create_client(url, key)

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


def doQuery(sql, params=None):
    """
    Executes an SQL query with the provided parameters.

    Parameters:
        sql (str): The SQL query to execute.
        params (tuple): Optional tuple of parameters to pass with the query.

    Returns:
        list: Query results as a list of rows (each row as a tuple).

    Example for a SELECT query:
    ```
    select_sql = "SELECT * FROM orders WHERE user = %s;"
    select_params = ('verityhub',)
    rows = doQuery(select_sql, select_params)
    print(rows)
    ```

    Example for an INSERT query :
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
                return cursor.fetchall()
            # Commit transaction for INSERT, UPDATE, DELETE
            connection.commit()
            return None  # Non-SELECT queries don't return rows

    except Exception as e:
        print(f"Query failed: {e}")
        connection.rollback()  # Rollback transaction on failure
        return None

    finally:
        release_connection(connection)


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
    rows = db.table("posts").select("id,content,user: users(id,full_name,handler,avatar)").order(
        column="created_at", desc=True).limit(10).execute()

    html = ""

    for row in rows.data:
        html += f"""
          <div class="post">
            <v-profile
            fullname="{row['user']['full_name']}" 
            handler="{row['user']['handler']}" 
            avatar="{row['user']['avatar']}"
            ></v-profile>
            <div class="content">
              {row['content']}
            </div>
          </div>
          """

    return html

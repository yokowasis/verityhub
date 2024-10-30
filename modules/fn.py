import os
from typing import List
from dotenv import load_dotenv
import psycopg2
import psycopg2.pool
from pydantic import BaseModel


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


class PostResult(BaseModel):
    id: int = 0
    full_name: str = ""
    username: str = ""
    avatar: str = ""
    content: str = ""


def getAllPosts(post_type: str, limit: int = 10, page: int = 1):
    offset = (page - 1) * limit
    sql = "SELECT posts.id, posts.content, users_auth.full_name, users_auth.username, users_auth.avatar FROM posts JOIN users_auth ON posts.username = users_auth.username WHERE type=%s ORDER BY posts.created_at DESC LIMIT %s OFFSET %s;"

    rows = doQuery(sql, (post_type, limit, offset))

    html = ""

    if (type(rows) == list):
        for row in rows:
            data = PostResult(**vars(row))

            html += f"""
            <div class="post" id="post-{data.id}">
              <v-profile
              fullname="{data.full_name}" 
              handler="{data.username}"
              avatar="{data.avatar}"
              ></v-profile>
              <div class="content">
                {data.content}
              </div>
              <div class="post-footer">
                <button onclick="addReply({data.id})" class="btn text-white reply-btn"><i class="fa fa-reply"></i> Reply</button>
              </div>
              <div id="reply-box-{data.id}">
              </div>
              <div class="replies" id="replies-{data.id}"></div>
            </div>
            """

    return html

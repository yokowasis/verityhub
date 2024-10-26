import http
import http.client
import json
import os
import urllib.parse
from dotenv import load_dotenv
from supabase import create_client, Client
import urllib

load_dotenv()


url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
db: Client = create_client(url, key)


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

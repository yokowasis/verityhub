import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
db: Client = create_client(url, key)


def getAllPosts():
    rows = db.table("posts").select("id,content,user: users(id,full_name,handler,avatar)").order(
        column="created_at", desc=False).limit(10).execute()

    html = ""

    for row in rows.data:
        html += f"""
          <div class="post">
            <v-profile
            fullname="{row['user']['full_name']}" 
            handler="${row['user']['handler']}" 
            avatar="{row['user']['avatar']}"
            ></v-profile>
            <div class="content">
              {row['content']}
            </div>
          </div>
          """

    return html

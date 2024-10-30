from typing import List

from pydantic import BaseModel
from modules.fn import PostResult, SQLRecord, doQuery

import torch
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

TRANSFORMER_MODEL = os.getenv('TRANSFORMER_MODEL')

model = SentenceTransformer(TRANSFORMER_MODEL)
openaimodel = os.getenv('OPENAI_MODEL') or "gpt-4o-mini"
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))


def translate(s: str, lang: str):
    completion = client.chat.completions.create(
        model=openaimodel,
        messages=[
            {"role": "system",
                "content": "you are a translator that translate input to " + lang},
            {"role": "user", "content": s}
        ]
    )
    return (completion.choices[0].message.content)


def summarize(s: str) -> str:
    completion = client.chat.completions.create(
        model=openaimodel,
        messages=[
            {
                "role": "system",
                "content": "You are a summarizer that summarize the text. \
                Limit to under 200 words."},
            {"role": "user", "content": s}
        ]
    )

    return (completion.choices[0].message.content or "Failed to Fetch Summary")


def arrayToString(array):
    s = "["
    for i in range(len(array)):
        s += str(array[i]) + ","
    s = s[:-1] + "]"
    return s


def stringToArray(s):
    s = s.replace("[", "")
    s = s.replace("]", "")
    s = s.split(",")
    v1 = [float(i) for i in s]
    return v1


def encodeEmbedding(sentence: str):
    return arrayToString(model.encode(sentence))


def cosineSimilarity(vec1, vec2):
    return torch.nn.functional.cosine_similarity(vec1, vec2)


def semanticSearch(text: str, limit: int = 10, page: int = 1):
    vec = encodeEmbedding(text)
    offset = (page - 1) * limit

    rows = doQuery(
        "SELECT posts.id, posts.content, users_auth.username, users_auth.full_name, users_auth.avatar FROM posts JOIN users_auth ON users_auth.username = posts.username ORDER BY posts.content_vec <-> %s LIMIT %s OFFSET %s;",
        (vec, limit, offset)
    )

    return rows


class SemanticSearchRes(BaseModel):
    id: int
    content: str
    username: str
    full_name: str
    avatar: str


def getSemanticSearchResult(text: str, limit: int = 10, page: int = 1):

    rows = semanticSearch(text, limit, page)

    html = ""

    if (type(rows) == list):
        for row in rows:

            data = SemanticSearchRes(**vars(row))

            html += f"""
            <div class="post">
              <v-profile
              fullname="{data.full_name}" 
              handler="{data.username}"
              avatar="{data.avatar}"
              ></v-profile>
              <div class="content">
                {data.content}
              </div>
            </div>
            """

    return html

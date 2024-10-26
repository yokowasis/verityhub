from typing import List

from pydantic import BaseModel
from modules.fn import doQuery

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

    return (completion.choices[0].message.content)


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


class SemanticSearchResult(BaseModel):
    id: int
    content: str
    username: str
    full_name: str
    avatar: str


def semanticSearch(text: str, limit: int = 10):
    vec = encodeEmbedding(text)
    rows: List[SemanticSearchResult] = doQuery(
        "SELECT posts.id, posts.content, users_auth.username, users_auth.full_name, users_auth.avatar FROM posts JOIN users_auth ON users_auth.username = posts.username ORDER BY posts.content_vec <-> %s LIMIT %s;",
        (vec, limit)
    )

    return rows


def getSemanticSearchResult(text: str, limit: int, page: int):

    rows = semanticSearch(text, limit)

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

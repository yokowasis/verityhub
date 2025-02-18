import json
from ollama import ChatResponse
from ollama import chat
from typing import List

from pydantic import BaseModel
from modules.fn import doQuery

import torch
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

TRANSFORMER_MODEL = os.getenv('TRANSFORMER_MODEL')
LLM_MODEL = os.getenv('LLM_MODEL') or 'llama3.2:1b'

model = SentenceTransformer(TRANSFORMER_MODEL)


def translate(s: str, lang: str = "english"):
    response: ChatResponse = chat(
        model='llama3.2:1b',
        messages=[
            {
              'role': 'user',
              'content': f'translate the text into {lang} : {s}',
            }],
        format={
            'type': 'object',
            'properties': {
                "translation": {
                    "type": "string"
                }
            },
            "required": ["translation"]
        }
    )

    json_response = json.loads(response['message']['content'])
    return (json_response['translation'])


def summarize(s: str) -> str:

    response: ChatResponse = chat(
        model='llama3.2:1b',
        messages=[
            {
              'role': 'user',
              'content': f'summarize this article into 1 paragraph : {s}',
            }],
        format={
            'type': 'object',
            'properties': {
                "summary": {
                    "type": "string"
                }
            },
            "required": ["summary"]
        }
    )

    json_response = json.loads(response['message']['content'])
    return (json_response['summary'])


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


def semanticSearch(text: str, limit: int = 10, page: int = 1, posttype: str = "post"):
    vec = encodeEmbedding(text)
    offset = (page - 1) * limit

    rows = doQuery(
        "SELECT posts.id, posts.content, users_auth.username, users_auth.full_name, users_auth.avatar FROM posts JOIN users_auth ON users_auth.username = posts.username WHERE type = %s ORDER BY posts.content_vec <-> %s LIMIT %s OFFSET %s;",
        (posttype, vec, limit, offset)
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

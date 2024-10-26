import torch
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = SentenceTransformer("WhereIsAI/UAE-Large-V1")
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


def summarize(s: str):
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


def encode(sentence: str):
    return arrayToString(model.encode(sentence))


def cosineSimilarity(vec1, vec2):
    return torch.nn.functional.cosine_similarity(vec1, vec2)

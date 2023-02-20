import openai
import numpy as np


# this function compare similarity between two vectors.
# The higher value the dot product have, the more alike between these vectors
def similarity(v1, v2):
    return np.dot(v1, v2)


# return a list of vectors
def embedding(content, engine='text-embedding-ada-002'):
    response = openai.Embedding.create(input=content, engine=engine)
    vector = response['data'][0]['embedding']
    return vector


def search_chunks(text, data, count=1):
    vector = embedding(text)
    points = []

    for item in data:
        # compare search terms with brain-data
        point = similarity(vector, item['vector'])
        points.append({
            'content': item['content'],
            'point': point
        })
    # sort points base on descendant order
    ordered = sorted(points, key=lambda d: d['point'], reverse=True)

    return ordered[0:count]


def gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temp,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=freq_penl,
        presence_penalty=pres_penl
    )
    text = response['choices'][0]['text'].strip()
    return text

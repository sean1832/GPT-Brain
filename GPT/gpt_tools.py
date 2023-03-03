import openai
import numpy as np
import requests
import sseclient


# this function compare similarity between two vectors.
# The higher value the dot product have, the more alike between these vectors
def similarity(v1, v2):
    return np.dot(v1, v2)


# return a list of vectors
def embedding(content, engine='text-embedding-ada-002'):
    response = openai.Embedding.create(input=content, engine=engine)
    vector = response['data'][0]['embedding']
    return vector


def search_chunks(query, data, count=1):
    vector = embedding(query)
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


def gpt3(prompt, model, params):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=params.temp,
        max_tokens=params.max_tokens,
        top_p=params.top_p,
        frequency_penalty=params.frequency_penalty,
        presence_penalty=params.present_penalty
    )
    text = response['choices'][0]['text'].strip()
    return text


def gpt3_stream(prompt, model, params):
    response = openai.Completion.create(
        model=model,
        stream=True,
        prompt=prompt,
        temperature=params.temp,
        max_tokens=params.max_tokens,
        top_p=params.top_p,
        frequency_penalty=params.frequency_penalty,
        presence_penalty=params.present_penalty
    )
    return response


def gpt35_stream(prompt, params, system_role_content: str = 'You are a helpful assistant.'):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=params.max_tokens,
        temperature=params.temp,
        top_p=params.top_p,
        frequency_penalty=params.frequency_penalty,
        presence_penalty=params.present_penalty,
        stream=True,
        messages=[
            {"role": "system", "content": system_role_content},
            {"role": "user", "content": prompt}
        ])
    return completions

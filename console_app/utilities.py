import json
import openai

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(content, filepath):
    with open(filepath, 'w') as file:
        file.write(content)

def write_json_file(content, filepath):
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=2)

def read_json_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# return a list of vectors
def embedding(content, engine='text-embedding-ada-002'):
    response = openai.Embedding.create(input=content, engine=engine)
    vector = response['data'][0]['embedding']
    return vector
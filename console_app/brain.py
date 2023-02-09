import openai
import numpy as np
import textwrap
import utilities

openai.api_key = utilities.open_file(r'.user\API-KEYS.txt').strip()
BRAIN_DATA = utilities.read_json_file(r'.user\brain-data.json')

# this function compare similarity between two vectors. 
# The higher value the dot product have, the more alike between these vectors
def similarity(v1, v2):
    return np.dot(v1, v2)

def search_chunks(text, data, count=1):
    vector = utilities.embedding(text)
    points = []

    for item in data:
        # compare search terms with brain-data
        point = similarity(vector, item['vector'])
        points.append({
            'content': item['content'],
            'point': point
        })
    # sort points base on decendent order
    ordered = sorted(points, key=lambda d: d['point'], reverse=True)

    return ordered[0:count]

def gpt3(prompt, model='text-davinci-003'):
    response = openai.Completion.create(
        model= model,
        prompt=prompt,
        temperature=0.1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response['choices'][0]['text'].strip()
    return text

def main():
    while True:

        query = input('\n\nAsk brain: ')
        results = search_chunks(query, BRAIN_DATA)
        answers = []
        answers_count = 0
        for result in results:
            my_info = utilities.open_file(r'prompt\my-info.txt')

            prompt = utilities.open_file(r'prompt\question.txt')
            prompt = prompt.replace('<<INFO>>', result['content'])
            prompt = prompt.replace('<<QS>>', query)
            prompt = prompt.replace('<<MY-INFO>>', my_info)

            answer = gpt3(prompt, model='text-davinci-003')
            answers.append(answer)
            answers_count += 1

        all_answers = '\n\n'.join(answers)
        print('\n\n============ANSWER============\n\n', all_answers)

        chunks = textwrap.wrap(all_answers, 10000)
        end = []
        for chunk in chunks:
            prompt = utilities.open_file(r'prompt\summarize.txt').replace('<<SUM>>', chunk)
            summary = gpt3(prompt, model='text-curie-001')
            end.append(summary)
        print('\n\n============SUMMRY============\n\n', '\n\n'.join(end))
if __name__ == '__main__':
    main()
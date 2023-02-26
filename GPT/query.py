import openai
import textwrap
import streamlit as st

import modules.utilities as util
import modules.language as language
import GPT
import modules.INFO as INFO

API_KEY = util.read_file(r'.user\API-KEYS.txt').strip()

openai.api_key = API_KEY

SESSION_LANG = st.session_state['SESSION_LANGUAGE']
_ = language.set_language()


def build(chunk_size=4000):
    openai.api_key = API_KEY
    all_text = util.read_file(r'.user\input.txt')

    # split text into smaller chunk of 4000 char each
    chunks = textwrap.wrap(all_text, chunk_size)
    chunk_count = len(chunks)
    result = []
    for idx, chunk in enumerate(chunks):
        embedding = GPT.gpt_tools.embedding(chunk.encode(encoding='ASCII', errors='ignore').decode())
        info = {'content': chunk, 'vector': embedding}
        print(info, '\n\n\n')

        result.append(info)
        # return index one at the time
        yield idx, chunk_count

    util.write_json(result, r'.user\brain-data.json')


def run(query, model, prompt_file, isQuestion, params, info_file=None):
    if isQuestion:
        data = util.read_json(INFO.BRAIN_DATA)
        results = GPT.gpt_tools.search_chunks(query, data, params.chunk_count)
        answers = []
        for result in results:
            my_info = util.read_file(info_file)
            prompt = util.read_file(prompt_file)
            prompt = prompt.replace('<<INFO>>', result['content'])
            prompt = prompt.replace('<<QS>>', query)
            prompt = prompt.replace('<<MY-INFO>>', my_info)

            answer = GPT.gpt_tools.gpt3(prompt, model, params)
            answers.append(answer)
        all_response = '\n\n'.join(answers)
    else:
        chunks = textwrap.wrap(query, 10000)
        responses = []
        for chunk in chunks:
            prompt = util.read_file(prompt_file).replace('<<DATA>>', chunk)
            response = GPT.gpt_tools.gpt3(prompt, model, params)
            responses.append(response)
        all_response = '\n\n'.join(responses)
    return all_response


def get_stream_prompt(query, prompt_file, isQuestion, info_file=None):
    openai.api_key = API_KEY
    if isQuestion:
        data = util.read_json(INFO.BRAIN_DATA)
        result = GPT.gpt_tools.search_chunks(query, data, count=1)
        my_info = util.read_file(info_file)
        prompt = util.read_file(prompt_file)
        prompt = prompt.replace('<<INFO>>', result[0]['content'])
        prompt = prompt.replace('<<QS>>', query)
        prompt = prompt.replace('<<MY-INFO>>', my_info)
    else:
        chunk = textwrap.wrap(query, 10000)[0]
        prompt = util.read_file(prompt_file).replace('<<DATA>>', chunk)
    return prompt


def run_stream(query, model, prompt_file, isQuestion, params, info_file=None):
    prompt = get_stream_prompt(query, prompt_file, isQuestion, info_file)
    client = GPT.gpt_tools.gpt3_stream(API_KEY, prompt, model, params)
    return client

import openai
import textwrap
import streamlit as st

import modules.utilities as util
import modules.language as language
import GPT

API_KEY = util.read_file(r'.user\API-KEYS.txt').strip()

openai.api_key = API_KEY

# if 'SESSION_LANGUAGE' not in st.session_state:
#     st.session_state['SESSION_LANGUAGE'] = util.read_json_at('.user/language.json', 'SESSION_LANGUAGE', 'en_US')

SESSION_LANG = st.session_state['SESSION_LANGUAGE']
prompt_dir = f'.user/prompt/{SESSION_LANG}'
_ = language.set_language()


def build(chunk_size=4000):
    all_text = util.read_file(r'.user\input.txt')

    # split text into smaller chunk of 4000 char each
    chunks = textwrap.wrap(all_text, chunk_size)
    chunk_count = len(chunks)
    result = []
    for idx, chunk in enumerate(chunks):
        embedding = GPT.toolkit.embedding(chunk.encode(encoding='ASCII', errors='ignore').decode())
        info = {'content': chunk, 'vector': embedding}
        print(info, '\n\n\n')

        result.append(info)
        # return index one at the time
        yield idx, chunk_count

    util.write_json(result, r'.user\brain-data.json')


def run_answer(query, model, temp, max_tokens, top_p, freq_penl, pres_penl, chunk_count):
    brain_data = util.read_json(r'.user\brain-data.json')
    results = GPT.toolkit.search_chunks(query, brain_data, chunk_count)
    answers = []
    for result in results:
        my_info = util.read_file(f'{prompt_dir}/' + _('my-info') + '.txt')

        prompt = util.read_file(f'{prompt_dir}/' + _('question') + '.txt')
        prompt = prompt.replace('<<INFO>>', result['content'])
        prompt = prompt.replace('<<QS>>', query)
        prompt = prompt.replace('<<MY-INFO>>', my_info)

        answer = GPT.toolkit.gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        answers.append(answer)

    all_answers = '\n\n'.join(answers)
    return all_answers


def run_answer_stream(query, model, temp, max_tokens, top_p, freq_penl, pres_penl):
    brain_data = util.read_json(r'.user\brain-data.json')
    results = GPT.toolkit.search_chunks(query, brain_data, count=1)
    for result in results:
        my_info = util.read_file(f'{prompt_dir}/' + _('my-info') + '.txt')
        prompt = util.read_file(f'{prompt_dir}/' + _('question') + '.txt')
        prompt = prompt.replace('<<INFO>>', result['content'])
        prompt = prompt.replace('<<QS>>', query)
        prompt = prompt.replace('<<MY-INFO>>', my_info)

        answer_client = GPT.toolkit.gpt3_stream(API_KEY, prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        return answer_client


def run(query, model, prompt_file, temp, max_tokens, top_p, freq_penl, pres_penl):
    chunks = textwrap.wrap(query, 10000)
    responses = []
    for chunk in chunks:
        prompt = util.read_file(prompt_file).replace('<<DATA>>', chunk)
        response = GPT.toolkit.gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        responses.append(response)
    all_response = '\n\n'.join(responses)
    return all_response


def run_stream(query, model, prompt_file, temp, max_tokens, top_p, freq_penl, pres_penl):
    chunk = textwrap.wrap(query, 10000)[0]
    prompt = util.read_file(prompt_file).replace('<<DATA>>', chunk)
    client = GPT.toolkit.gpt3_stream(API_KEY, prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
    return client

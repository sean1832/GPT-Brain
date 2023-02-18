import openai
import textwrap

from modules import utilities as util
from modules import language
import streamlit as st
from modules import gpt_util as gpt

openai.api_key = util.read_file(r'.user\API-KEYS.txt').strip()

if 'SESSION_LANGUAGE' not in st.session_state:
    st.session_state['SESSION_LANGUAGE'] = util.read_json_at('.user/language.json', 'SESSION_LANGUAGE', 'en_US')

SESSION_LANG = st.session_state['SESSION_LANGUAGE']
prompt_dir = f'.user/prompt/{SESSION_LANG}'
_ = language.set_language()


def build(chunk_size=4000):
    all_text = util.read_file(r'.user\input.txt')

    # split text into smaller chunk of 4000 char each
    chunks = textwrap.wrap(all_text, chunk_size)

    result = []

    print('Building brain data...')
    for chunk in chunks:
        embedding = gpt.embedding(chunk.encode(encoding='ASCII', errors='ignore').decode())
        info = {'content': chunk, 'vector': embedding}
        print(info, '\n\n\n')
        result.append(info)

    util.write_json(result, r'.user\brain-data.json')


def run_answer(query, model, temp, max_tokens, top_p, freq_penl, pres_penl, chunk_count):
    brain_data = util.read_json(r'.user\brain-data.json')
    results = gpt.search_chunks(query, brain_data, chunk_count)
    answers = []
    for result in results:
        my_info = util.read_file(f'{prompt_dir}/' + _('my-info') + '.txt')

        prompt = util.read_file(f'{prompt_dir}/' + _('question') + '.txt')
        prompt = prompt.replace('<<INFO>>', result['content'])
        prompt = prompt.replace('<<QS>>', query)
        prompt = prompt.replace('<<MY-INFO>>', my_info)

        answer = gpt.gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        answers.append(answer)

    all_answers = '\n\n'.join(answers)
    return all_answers


def run(query, model, prompt_file, temp, max_tokens, top_p, freq_penl, pres_penl):
    chunks = textwrap.wrap(query, 10000)
    responses = []
    for chunk in chunks:
        prompt = util.read_file(prompt_file).replace('<<DATA>>', chunk)
        response = gpt.gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        responses.append(response)
    all_response = '\n\n'.join(responses)
    return all_response

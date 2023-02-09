import openai
import textwrap

from modules import utilities as util
from modules import gpt_util as gpt

openai.api_key = util.read_file(r'.user\API-KEYS.txt').strip()
BRAIN_DATA = util.read_json_file(r'.user\brain-data.json')
prompt_dir = '.user/prompt'


def build(chunk_size=4000):
    all_text = util.read_file(r'.user\input.txt')

    # split text into smaller chunk of 4000 char each
    chunks = textwrap.wrap(all_text, chunk_size)

    result = []

    for chunk in chunks:
        embedding = gpt.embedding(chunk.encode(encoding='ASCII', errors='ignore').decode())
        info = {'content': chunk, 'vector': embedding}
        print(info, '\n\n\n')
        result.append(info)

    util.write_json_file(result, r'.user\brain-data.json')


def run_answer(query, model, temp, max_tokens, top_p, freq_penl, pres_penl, chunk_count):
    results = gpt.search_chunks(query, BRAIN_DATA, chunk_count)
    answers = []
    for result in results:
        my_info = util.read_file(f'{prompt_dir}/my-info.txt')

        prompt = util.read_file(f'{prompt_dir}/question.txt')
        prompt = prompt.replace('<<INFO>>', result['content'])
        prompt = prompt.replace('<<QS>>', query)
        prompt = prompt.replace('<<MY-INFO>>', my_info)

        answer = gpt.gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        answers.append(answer)

    all_answers = '\n\n'.join(answers)
    # print('\n\n============ANSWER============\n\n', all_answers)
    return all_answers


def run_summary(query, model, temp, max_tokens, top_p, freq_penl, pres_penl):
    chunks = textwrap.wrap(query, 10000)
    summaries = []
    for chunk in chunks:
        prompt = util.read_file(f'{prompt_dir}/summarize.txt').replace('<<SUM>>', chunk)
        summary = gpt.gpt3(prompt, model, temp, max_tokens, top_p, freq_penl, pres_penl)
        summaries.append(summary)
    all_summary = '\n\n'.join(summaries)
    # print('\n\n============SUMMRY============\n\n', all_summary)
    return all_summary

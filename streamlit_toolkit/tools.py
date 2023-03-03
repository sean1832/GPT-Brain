import os
import time
import json
import streamlit as st
import tkinter as tk
from tkinter import filedialog
from langchain.llms import OpenAI

import modules.utilities as util
import modules.INFO as INFO
import modules as mod
import GPT

if 'SESSION_TIME' not in st.session_state:
    st.session_state['SESSION_TIME'] = time.strftime("%Y%m%d-%H%H%S")

_ = mod.language.set_language()
SESSION_TIME = st.session_state['SESSION_TIME']
CURRENT_LOG_FILE = f'{INFO.LOG_PATH}/log_{SESSION_TIME}.log'


def predict_token(query: str, prompt_core: GPT.model.prompt_core) -> int:
    """predict how many tokens to generate"""
    llm = OpenAI()
    token = llm.get_num_tokens(GPT.query.get_stream_prompt(query, prompt_file=prompt_core.question,
                                                           isQuestion=True,
                                                           info_file=prompt_core.my_info))
    return token


def create_log():
    if not os.path.exists(CURRENT_LOG_FILE):
        util.write_file(f'Session {SESSION_TIME}\n\n', CURRENT_LOG_FILE)
    return CURRENT_LOG_FILE


def log(content, delimiter=''):
    log_file = create_log()
    if delimiter != '':
        delimiter = f'\n\n=============={delimiter}==============\n'
    util.write_file(f'\n{delimiter + content}', log_file, 'a')


def clear_log():
    log_file_name = f'log_{SESSION_TIME}.log'
    for root, dirs, files in os.walk(INFO.LOG_PATH):
        for file in files:
            if not file == log_file_name:
                os.remove(os.path.join(root, file))


def download_as(label):
    # download log file
    with open(CURRENT_LOG_FILE, 'rb') as f:
        content = f.read()
        st.download_button(
            label=label,
            data=content,
            file_name=f'log_{SESSION_TIME}.txt',
            mime='text/plain'
        )


def save(content, path, page='', json_value: dict = None):
    if json_value is None:
        json_value = []
    save_but = st.button(_('💾Save'))
    if save_but:
        util.write_file(content, path)
        st.success(_('✅File saved!'))
        # write to json file
        if page == '💽Brain Memory':
            for key, value in json_value.items():
                util.update_json(INFO.BRAIN_MEMO, key, value)

        time.sleep(1)
        # refresh page
        st.experimental_rerun()


def match_logic(operator, filter_val, value):
    if operator == 'IS':
        return filter_val == value
    elif operator == 'IS NOT':
        return filter_val != value
    elif operator == 'CONTAINS':
        return filter_val in value
    elif operator == 'NOT CONTAINS':
        return filter_val not in value
    elif operator == 'MORE THAN':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) < float(value)
    elif operator == 'LESS THAN':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) > float(value)
    elif operator == 'MORE THAN OR EQUAL':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) <= float(value)
    elif operator == 'LESS THAN OR EQUAL':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) >= float(value)
    else:
        return False


def select_directory(initial_dir=os.getcwd()):
    root = tk.Tk()
    root.withdraw()
    # make sure the dialog is on top of the main window
    root.attributes('-topmost', True)
    directory = filedialog.askdirectory(initialdir=initial_dir, title=_('Select Note Directory'), master=root)
    return directory


def match_fields(pages: list, filter_datas: list[dict]):
    filtered_contents = []
    for page in pages:
        fields = util.extract_frontmatter(page, delimiter='---')
        found_data = []
        for field in fields:
            if field == '':
                continue
            try:
                found_key, found_value = field.split(': ')
            except ValueError:
                continue
            found_key = found_key.strip()
            found_value = found_value.strip()

            found_data.append({
                'key': found_key,
                'value': found_value
            })

        found_match = []
        for data in filter_datas:
            for found in found_data:
                data_key = data['key'].lower()
                data_val = data['value'].lower()
                found_key = found['key'].lower()
                found_val = found['value'].lower()
                if data_key == found_key:
                    if match_logic(data['logic'], data_val, found_val):
                        # found single match
                        found_match.append(True)

        # if all match
        if found_match.count(True) == len(filter_datas):
            filtered_contents.append(page)

    combined_contents = '\n\n\n\n'.join(filtered_contents)
    return combined_contents


def add_filter(num, val_filter_key, val_filter_logic, val_filter_val):
    # filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_key = st.text_input(f'Key{num}', placeholder='Key', value=val_filter_key)
    with col2:
        options = ['CONTAINS',
                   'NOT CONTAINS',
                   'IS',
                   'IS NOT',
                   'MORE THAN',
                   'LESS THAN',
                   'MORE THAN OR EQUAL',
                   'LESS THAN OR EQUAL']
        default_index = util.get_index(options, val_filter_logic, 0)
        logic_select = st.selectbox(f'Logic{num}', options, index=default_index)
    with col3:
        if isinstance(val_filter_val, int):
            val_filter_val = "{:02}".format(val_filter_val)
        filter_val = st.text_input(f'value{num}', placeholder='Value', value=val_filter_val)
    return filter_key, logic_select, filter_val


def filter_data(pages: list, add_filter_button, del_filter_button):
    init_filter_infos = util.read_json_at(INFO.BRAIN_MEMO, 'filter_info')

    filter_datas = []
    if add_filter_button:
        st.session_state['FILTER_ROW_COUNT'] += 1
    if del_filter_button:
        st.session_state['FILTER_ROW_COUNT'] -= 1
    if st.session_state['FILTER_ROW_COUNT'] >= 1:
        for i in range(st.session_state['FILTER_ROW_COUNT'] + 1):
            try:
                init_info = init_filter_infos[i - 1]
                init_key = init_info['key']
                init_logic = init_info['logic']
                init_val = init_info['value']
            except IndexError:
                init_key = ''
                init_logic = 'CONTAINS'
                init_val = ''
            except KeyError:
                init_key = ''
                init_logic = 'CONTAINS'
                init_val = ''

            if i == 0:
                continue
            # add filter
            filter_key, logic_select, filter_val = add_filter(i, init_key, init_logic, init_val)
            data = {'key': filter_key, 'logic': logic_select, 'value': filter_val}
            filter_datas.append(data)

    # filter data
    filtered_contents = match_fields(pages, filter_datas)
    return filtered_contents, filter_datas


def process_response(query, target_model, prompt_file: str, params: GPT.model.param):
    # check if exclude model is not target model
    file_name = util.get_file_name(prompt_file)
    with st.spinner(_('Thinking on ') + f"{file_name}..."):
        results = GPT.query.run(query,
                                target_model,
                                prompt_file,
                                isQuestion=False,
                                params=params)
        # displaying results
        st.header(f'📃{file_name}')
        st.info(f'{results}')
        time.sleep(1)
        log(results, delimiter=f'{file_name.upper()}')


def process_response_stream(query, target_model, prompt_file: str, params: GPT.model.param):
    # check if exclude model is not target model
    file_name = util.get_file_name(prompt_file)
    with st.spinner(_('Thinking on ') + f"{file_name}..."):
        responses = GPT.query.run_stream(query,
                                         target_model,
                                         prompt_file,
                                         isQuestion=False,
                                         params=params)

    # displaying results
    st.header(f'📃{file_name}')
    response_panel = st.empty()
    previous_chars = ''
    for response_json in responses:
        choice = response_json['choices'][0]
        if choice['finish_reason'] == 'stop':
            break
        # error handling
        if choice['finish_reason'] == 'length':
            st.warning("⚠️ " + _('Result cut off. max_tokens') + f' ({params.max_tokens}) ' + _('too small. Consider increasing max_tokens.'))
            break
        char = choice['text']
        response = previous_chars + char
        response_panel.info(f'{response}')
        previous_chars += char

    time.sleep(1)
    log(previous_chars, delimiter=f'{file_name.upper()}')


def rebuild_brain(chunk_size: int):
    msg = st.warning(_('Updating Brain...'), icon="⏳")
    progress_bar = st.progress(0)
    for idx, chunk_num in GPT.query.build(chunk_size):
        progress_bar.progress((idx + 1) / chunk_num)
    msg.success(_('Brain Updated!'), icon="👍")
    time.sleep(2)


def execute_brain(q, params: GPT.model.param,
                  op: GPT.model.Operation,
                  model: GPT.model.Model,
                  prompt_core: GPT.model.prompt_core,
                  prompt_dictionary: dict,
                  question_prompt: str,
                  stream: bool
                  ):
    # log question
    log(f'\n\n\n\n[{str(time.ctime())}] - QUESTION: {q}')

    if mod.check_update.is_input_updated() or mod.check_update.is_param_updated(params.chunk_size, 'chunk_size'):
        rebuild_brain(params.chunk_size)

    # =================stream=================
    if stream:
        previous_chars = ''
        is_question_selected = util.contains(op.operations, question_prompt)
        with st.spinner(_('Thinking on Answer')):
            responses = GPT.query.run_stream(q, model.question_model,
                                             prompt_file=prompt_core.question,
                                             isQuestion=True,
                                             params=params,
                                             info_file=prompt_core.my_info)
        if is_question_selected:
            # displaying results
            st.header(_('💬Answer'))

        answer_panel = st.empty()
        for response_json in responses:
            choice = response_json['choices'][0]
            if choice['finish_reason'] == 'stop':
                break
            # error handling
            if choice['finish_reason'] == 'length':
                st.warning("⚠️ " + _('Result cut off. max_tokens') + f' ({params.max_tokens}) ' + _('too small. Consider increasing max_tokens.'))
                break

            char = choice['text']
            answer = previous_chars + char
            if is_question_selected:
                answer_panel.info(f'{answer}')
            previous_chars += char

        time.sleep(0.1)
        log(previous_chars, delimiter='ANSWER')
        if len(op.operations_no_question) > 0:
            for i in range(len(op.operations_no_question)):
                prompt_path = prompt_dictionary[op.operations_no_question[i]]
                other_model = model.other_models[i]
                process_response_stream(previous_chars, other_model, prompt_path, params)
    # =================stream=================
    else:
        # thinking on answer
        with st.spinner(_('Thinking on Answer')):
            responses = GPT.query.run(q, model.question_model,
                                      prompt_file=prompt_core.question,
                                      isQuestion=True,
                                      params=params,
                                      info_file=prompt_core.my_info)
            if util.contains(op.operations, question_prompt):
                # displaying results
                st.header(_('💬Answer'))
                st.info(f'{responses}')
                time.sleep(1.5)
                log(responses, delimiter='ANSWER')

        # thinking on other outputs
        if len(op.operations_no_question) > 0:
            for i in range(len(op.operations_no_question)):
                prompt_path = prompt_dictionary[op.operations_no_question[i]]
                other_model = model.other_models[i]
                process_response(responses, other_model, prompt_path, params)


def message(msg, condition=None):
    if condition is not None:
        if condition:
            st.warning("⚠️" + msg)
    else:
        st.warning("⚠️" + msg)

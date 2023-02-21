import os
import time
import streamlit as st
import tkinter as tk
from tkinter import filedialog

import modules.utilities as util
import modules.INFO as INFO
import modules as mod
import GPT

if 'SESSION_TIME' not in st.session_state:
    st.session_state['SESSION_TIME'] = time.strftime("%Y%m%d-%H%H%S")

_ = mod.language.set_language()
SESSION_TIME = st.session_state['SESSION_TIME']
CURRENT_LOG_FILE = f'{INFO.LOG_PATH}/log_{SESSION_TIME}.log'


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


def download_as():
    # download log file
    with open(CURRENT_LOG_FILE, 'rb') as f:
        content = f.read()
        st.download_button(
            label=_("📥download log"),
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
            util.update_json(INFO.BRAIN_MEMO, 'delimiter', json_value['delimiter'])
            util.update_json(INFO.BRAIN_MEMO, 'append_mode', json_value['append_mode'])
            util.update_json(INFO.BRAIN_MEMO, 'force_mode', json_value['force_mode'])
            util.update_json(INFO.BRAIN_MEMO, 'advanced_mode', json_value['advanced_mode'])
            util.update_json(INFO.BRAIN_MEMO, 'filter_info', json_value['filter_info'])
            util.update_json(INFO.BRAIN_MEMO, 'filter_row_count', json_value['filter_row_count'])
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


def select_directory():
    root = tk.Tk()
    root.withdraw()
    # make sure the dialog is on top of the main window
    root.attributes('-topmost', True)
    directory = filedialog.askdirectory(initialdir=os.getcwd(), title=_('Select Note Directory'), master=root)
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


def process_response(query, target_model, prompt_file: str, data: GPT.model.param):
    # check if exclude model is not target model
    file_name = util.get_file_name(prompt_file)
    with st.spinner(_('Thinking on ') + f"{file_name}..."):
        results = GPT.query.run(query, target_model, prompt_file,
                                data.temp,
                                data.max_tokens,
                                data.top_p,
                                data.frequency_penalty,
                                data.present_penalty)
        # displaying results
        st.header(f'📃{file_name}')
        st.info(f'{results}')
        time.sleep(1)
        log(results, delimiter=f'{file_name.upper()}')


def execute_brain(q, params: GPT.model.param,
                  op: GPT.model.Operation,
                  model: GPT.model.Model,
                  prompt_dictionary: dict,
                  session_language):
    # log question
    log(f'\n\n\n\n[{str(time.ctime())}] - QUESTION: {q}')

    if mod.check_update.isUpdated():
        st.success(_('Building Brain...'))
        # if brain-info is updated
        GPT.query.build(params.chunk_size)
        st.success(_('Brain rebuild!'))
        time.sleep(2)

    # thinking on answer
    with st.spinner(_('Thinking on Answer')):
        answer = GPT.query.run_answer(q, model.question_model,
                                      params.temp,
                                      params.max_tokens,
                                      params.top_p,
                                      params.frequency_penalty,
                                      params.present_penalty,
                                      chunk_count=params.chunk_count)
        if util.contains(op.operations, _('question')):
            # displaying results
            st.header(_('💬Answer'))
            st.info(f'{answer}')
            time.sleep(1)
            log(answer, delimiter='ANSWER')

    # thinking on other outputs
    if len(op.operations_no_question) > 0:
        for i in range(len(op.operations_no_question)):
            prompt_path = prompt_dictionary[op.operations_no_question[i]]
            other_model = model.other_models[i]
            process_response(answer, other_model, prompt_path, params)
    # convert param to dictionary
    param_dict = vars(params)

    # write param to json
    for key in param_dict:
        value = param_dict[key]
        util.update_json(INFO.BRAIN_MEMO, key, value)

    # write operation to json
    util.update_json(INFO.BRAIN_MEMO, f'operations_{session_language}', op.operations)

    # write question model to json
    util.update_json(INFO.BRAIN_MEMO, 'question_model', model.question_model)

    # write other models to json
    for i in range(len(op.operations_no_question)):
        util.update_json(INFO.BRAIN_MEMO, f'{op.operations_no_question[i]}_model', model.other_models[i])


def message(msg, condition=None):
    if condition is not None:
        if condition:
            st.warning("⚠️" + msg)
    else:
        st.warning("⚠️" + msg)

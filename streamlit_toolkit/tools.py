import os
import time
import streamlit as st

import modules.utilities as util
import modules.INFO as INFO
import modules as mod
import GPT

_ = mod.language.set_language()


def create_log():
    if not os.path.exists(INFO.CURRENT_LOG_FILE):
        util.write_file(f'Session {INFO.SESSION_TIME}\n\n', INFO.CURRENT_LOG_FILE)
    return INFO.CURRENT_LOG_FILE


def log(content, delimiter=''):
    log_file = create_log()
    if delimiter != '':
        delimiter = f'\n\n=============={delimiter}==============\n'
    util.write_file(f'\n{delimiter + content}', log_file, 'a')


def clear_log():
    log_file_name = f'log_{INFO.SESSION_TIME}.log'
    for root, dirs, files in os.walk(INFO.LOG_PATH):
        for file in files:
            if not file == log_file_name:
                os.remove(os.path.join(root, file))


def save_as():
    # download log file
    with open(INFO.CURRENT_LOG_FILE, 'rb') as f:
        content = f.read()
        st.download_button(
            label=_("📥download log"),
            data=content,
            file_name=f'log_{INFO.SESSION_TIME}.txt',
            mime='text/plain'
        )


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

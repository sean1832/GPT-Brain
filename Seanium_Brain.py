import time
import os

import streamlit as st

import modules as mod
import GPT
import modules.utilities as util
import modules.INFO as INFO

SESSION_LANG = st.session_state['SESSION_LANGUAGE']
PROMPT_PATH = f'.user/prompt/{SESSION_LANG}'


util.remove_oldest_file(INFO.LOG_PATH, 10)

header = st.container()
body = st.container()


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


def process_response(query, target_model, prompt_file: str, data: GPT.model_param.param):
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


def message(msg, condition=None):
    if condition is not None:
        if condition:
            st.warning("⚠️" + msg)
    else:
        st.warning("⚠️" + msg)


# sidebar
with st.sidebar:
    _ = mod.language.set_language()
    st.title(_('Settings'))
    mod.language.select_language()

    prompt_files = util.scan_directory(PROMPT_PATH)
    prompt_file_names = [util.get_file_name(file) for file in prompt_files]
    prompt_dictionary = dict(zip(prompt_file_names, prompt_files))
    # remove 'my-info' from prompt dictionary
    prompt_dictionary.pop(_('my-info'))

    operation_options = list(prompt_dictionary.keys())
    operations = st.multiselect(_('Operations'), operation_options,
                                default=util.read_json_at(INFO.BRAIN_MEMO, f'operations_{SESSION_LANG}',
                                                          operation_options[0]))

    last_question_model = util.read_json_at(INFO.BRAIN_MEMO, 'question_model', INFO.MODELS_OPTIONS[0])
    # get index of last question model
    question_model_index = util.get_index(INFO.MODELS_OPTIONS, last_question_model)
    question_model = st.selectbox(_('Question Model'), INFO.MODELS_OPTIONS, index=question_model_index)

    operations_no_question = [op for op in operations if op != _('question')]
    other_models = []
    replace_tokens = []
    for operation in operations_no_question:
        last_model = util.read_json_at(INFO.BRAIN_MEMO, f'{operation}_model', INFO.MODELS_OPTIONS[0])
        # get index of last model
        model_index = util.get_index(INFO.MODELS_OPTIONS, last_model)
        model = st.selectbox(f"{operation} " + _('Model'), INFO.MODELS_OPTIONS, index=model_index)
        other_models.append(model)

    temp = st.slider(_('Temperature'), 0.0, 1.0, value=util.read_json_at(INFO.BRAIN_MEMO, 'temp', 0.1))
    max_tokens = st.slider(_('Max Tokens'), 850, 4500, value=util.read_json_at(INFO.BRAIN_MEMO, 'max_tokens', 1000))

    with st.expander(label=_('Advanced Options')):
        top_p = st.slider(_('Top_P'), 0.0, 1.0, value=util.read_json_at(INFO.BRAIN_MEMO, 'top_p', 1.0))
        freq_panl = st.slider(_('Frequency penalty'), 0.0, 1.0,
                              value=util.read_json_at(INFO.BRAIN_MEMO, 'frequency_penalty', 0.0))
        pres_panl = st.slider(_('Presence penalty'), 0.0, 1.0,
                              value=util.read_json_at(INFO.BRAIN_MEMO, 'present_penalty', 0.0))

        chunk_size = st.slider(_('Chunk size'), 1500, 4500,
                               value=util.read_json_at(INFO.BRAIN_MEMO, 'chunk_size', 4000))
        chunk_count = st.slider(_('Answer count'), 1, 5, value=util.read_json_at(INFO.BRAIN_MEMO, 'chunk_count', 1))

    param = GPT.model_param.param(temp=temp,
                                  max_tokens=max_tokens,
                                  top_p=top_p,
                                  frequency_penalty=freq_panl,
                                  present_penalty=pres_panl,
                                  chunk_size=chunk_size,
                                  chunk_count=chunk_count)

    if st.button(_('Clear Log'), on_click=clear_log):
        st.success(_('Log Cleared'))

    # info
    st.markdown('---')
    st.markdown(f"# {util.read_json_at(INFO.MANIFEST, 'name')}")
    st.markdown(_('Version') + f": {util.read_json_at(INFO.MANIFEST, 'version')}")
    st.markdown(_('Author') + f": {util.read_json_at(INFO.MANIFEST, 'author')}")
    st.markdown("[" + _('Report bugs') + "]" + f"({util.read_json_at(INFO.MANIFEST, 'bugs')})")
    st.markdown("[" + _('Github Repo') + "]" + f"({util.read_json_at(INFO.MANIFEST, 'homepage')})")

with header:
    st.title(_('🧠GPT-Brain'))
    st.text(_('This is my personal AI powered brain feeding my own Obsidian notes. Ask anything.'))

    message(_("This is a beta version. Please [🪲report bugs](") + util.read_json_at(INFO.MANIFEST, 'bugs') + _(
        ") if you find any."))


def execute_brain(q):
    # log question
    log(f'\n\n\n\n[{str(time.ctime())}] - QUESTION: {q}')

    if mod.check_update.isUpdated():
        st.success(_('Building Brain...'))
        # if brain-info is updated
        GPT.query.build(chunk_size)
        st.success(_('Brain rebuild!'))
        time.sleep(2)

    # thinking on answer
    with st.spinner(_('Thinking on Answer')):
        answer = GPT.query.run_answer(q, question_model, temp, max_tokens, top_p, freq_panl, pres_panl,
                                      chunk_count=chunk_count)
        if util.contains(operations, _('question')):
            # displaying results
            st.header(_('💬Answer'))
            st.info(f'{answer}')
            time.sleep(1)
            log(answer, delimiter='ANSWER')

    # thinking on other outputs
    if len(operations_no_question) > 0:
        for i in range(len(operations_no_question)):
            prompt_path = prompt_dictionary[operations_no_question[i]]
            other_model = other_models[i]
            process_response(answer, other_model, prompt_path, param)
    # convert param to dictionary
    param_dict = vars(param)

    # write param to json
    for key in param_dict:
        value = param_dict[key]
        util.update_json(INFO.BRAIN_MEMO, key, value)

    # write operation to json
    util.update_json(INFO.BRAIN_MEMO, f'operations_{SESSION_LANG}', operations)

    # write question model to json
    util.update_json(INFO.BRAIN_MEMO, 'question_model', question_model)

    # write other models to json
    for i in range(len(operations_no_question)):
        util.update_json(INFO.BRAIN_MEMO, f'{operations_no_question[i]}_model', other_models[i])


# main
with body:
    question = st.text_area(_('Ask Brain: '))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        send = st.button(_('📩Send'))
    with col2:
        if os.path.exists(INFO.CURRENT_LOG_FILE):
            save_as()
    # execute brain calculation
    if not question == '' and send:
        execute_brain(question)

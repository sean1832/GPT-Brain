import os

import streamlit as st

import modules.INFO as INFO
import modules as mod
import GPT
import modules.utilities as util
import streamlit_toolkit.tools as st_tool

SESSION_LANG = st.session_state['SESSION_LANGUAGE']
PROMPT_PATH = f'.user/prompt/{SESSION_LANG}'

util.remove_oldest_file(INFO.LOG_PATH, 10)

header = st.container()
body = st.container()

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

    param = GPT.model.param(temp=temp,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            frequency_penalty=freq_panl,
                            present_penalty=pres_panl,
                            chunk_size=chunk_size,
                            chunk_count=chunk_count)

    op = GPT.model.Operation(operations=operations,
                             operations_no_question=operations_no_question)

    models = GPT.model.Model(question_model=question_model,
                             other_models=other_models)

    if st.button(_('Clear Log'), on_click=st_tool.clear_log):
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

    st_tool.message(_("This is a beta version. Please [🪲report bugs](") +
                    util.read_json_at(INFO.MANIFEST, 'bugs') + _(") if you find any."))

# main
with body:
    question = st.text_area(_('Ask Brain: '))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        send = st.button(_('📩Send'))
    with col2:
        if os.path.exists(INFO.CURRENT_LOG_FILE):
            st_tool.download_as()
    # execute brain calculation
    if not question == '' and send:
        st_tool.execute_brain(question, param, op, models, prompt_dictionary, SESSION_LANG)

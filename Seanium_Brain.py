import os

import streamlit as st
import streamlit_toggle as st_toggle

import modules.INFO as INFO
import modules as mod
import GPT
import modules.utilities as util
import streamlit_toolkit.tools as st_tool

SESSION_TIME = st.session_state['SESSION_TIME']
SESSION_LANG = st.session_state['SESSION_LANGUAGE']

PROMPT_PATH = f'.user/prompt/{SESSION_LANG}'
CURRENT_LOG_FILE = f'{INFO.LOG_PATH}/log_{SESSION_TIME}.log'

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
    operations = st.multiselect(_('Operations'),
                                operation_options,
                                default=util.read_json_at(INFO.BRAIN_MEMO, f'operations_{SESSION_LANG}',
                                                          _('question')),
                                help=_('Combinations of operations to perform.'))

    last_question_model = util.read_json_at(INFO.BRAIN_MEMO, 'question_model', INFO.MODELS_OPTIONS[0])
    # get index of last question model
    question_model_index = util.get_index(INFO.MODELS_OPTIONS, last_question_model)
    question_model = st.selectbox(_('Question Model'), INFO.MODELS_OPTIONS, index=question_model_index,
                                  help=_('Model used for answering user question.'))

    operations_no_question = [op for op in operations if op != _('question')]
    other_models = []
    replace_tokens = []
    for operation in operations_no_question:
        last_model = util.read_json_at(INFO.BRAIN_MEMO, f'{operation}_model', INFO.MODELS_OPTIONS[0])
        # get index of last model
        model_index = util.get_index(INFO.MODELS_OPTIONS, last_model)
        model = st.selectbox(f"{operation} " + _('Model'), INFO.MODELS_OPTIONS, index=model_index)
        other_models.append(model)

    temp = st.slider(_('Temperature'), 0.0, 1.0, value=util.read_json_at(INFO.BRAIN_MEMO, 'temp', 0.1),
                     help=_('What sampling temperature to use, between 0 and 1. Higher values like 0.8 will make the '
                            'output more random, while lower values like 0.2 will make it more focused and '
                            'deterministic. \n\nIt is generally recommend altering this or `top_p` but not both.'))
    max_tokens = st.slider(_('Max Tokens'), 850, 4096, value=util.read_json_at(INFO.BRAIN_MEMO, 'max_tokens', 1000),
                           help=_("The maximum number of tokens to generate in the completion.\n\nThe token count of "
                                  "your prompt plus `max_tokens` cannot exceed the model's context length. Most "
                                  "models have a context length of 2048 tokens (except for the newest models, "
                                  "which support 4096)."))

    with st.expander(label=_('Advanced Options')):
        top_p = st.slider(_('Top_P'), 0.0, 1.0, value=util.read_json_at(INFO.BRAIN_MEMO, 'top_p', 1.0),
                          help=_("An alternative to sampling with temperature, called nucleus sampling, where the "
                                 "model considers the results of the tokens with top_p probability mass. So 0.1 means "
                                 "only the tokens comprising the top 10% probability mass are considered.\n\n"
                                 "It is generally recommend altering this or `temperature` but not both."))
        freq_panl = st.slider(_('Frequency penalty'), 0.0, 2.0,
                              value=util.read_json_at(INFO.BRAIN_MEMO, 'frequency_penalty', 0.0),
                              help=_("Larger the number increasing the model's likelihood to talk about new topics. "
                                     "Penalize new tokens based on whether they appear in the text so far."
                                     "\n\n[See more information about frequency and presence penalties.]"
                                     "(https://platform.openai.com/docs/api-reference/parameter-details)"))
        pres_panl = st.slider(_('Presence penalty'), 0.0, 1.0,
                              value=util.read_json_at(INFO.BRAIN_MEMO, 'present_penalty', 0.0),
                              help=_("Decreasing the model's likelihood to repeat the same line verbatim. Penalize "
                                     "new tokens based on their existing frequency in the text so far."
                                     "\n\n[See more information about frequency and presence penalties.]"
                                     "(https://platform.openai.com/docs/api-reference/parameter-details)"))

        chunk_size = st.slider(_('Chunk size'), 1500, 4500,
                               value=util.read_json_at(INFO.BRAIN_MEMO, 'chunk_size', 4000),
                               help=_("The number of tokens to consider at each step. The larger this is, the more "
                                      "context the model has to work with, but the slower generation and expensive "
                                      "will it be."))
        enable_stream = st_toggle.st_toggle_switch(_('Stream (experimental)'),
                                                   default_value=util.read_json_at(INFO.BRAIN_MEMO, 'enable_stream',
                                                                                   False))

        if not enable_stream:
            chunk_count = st.slider(_('Answer count'), 1, 5, value=util.read_json_at(INFO.BRAIN_MEMO, 'chunk_count', 1),
                                    help=_("The number of answers to generate. The model will continue to iteratively "
                                           "generating answers until it reaches the answer count."
                                           "\n\nNote that this function does not supports `stream` mode."))
        else:
            chunk_count = 1
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

    prompt_core = GPT.model.prompt_core(question=f'{PROMPT_PATH}/' + _('question') + '.txt',
                                        my_info=f'{PROMPT_PATH}/' + _('my-info') + '.txt')

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
    col1, col2 = st.columns([1, 3])
    with col1:
        send = st.button(_('📩Send'))
    with col2:
        if os.path.exists(CURRENT_LOG_FILE):
            st_tool.download_as(_("📥download log"))
    # execute brain calculation
    if not question == '' and send:
        st_tool.execute_brain(question,
                              param,
                              op,
                              models,
                              prompt_core,
                              prompt_dictionary,
                              _('question'),
                              enable_stream,
                              SESSION_LANG)

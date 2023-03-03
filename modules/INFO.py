import streamlit as st

import modules.utilities as util

st.set_page_config(
    page_title='GPT Brain'
)

# path
USER_DIR = '.user'
LOG_PATH = '.user/log'
BRAIN_MEMO = '.user/brain-memo.json'
BRAIN_DATA = '.user/brain-data.json'
MANIFEST = '.core/manifest.json'
INIT_LANGUAGE = '.user/language.json'

# exclude directory
EXCLUDE_DIR_OFFICIAL = ['__pycache__',
                        '.git',
                        '.idea',
                        '.vscode',
                        '.obsidian',
                        '.trash',
                        '.git',
                        '.gitignore',
                        '.gitattributes']

# activate session
if 'SESSION_LANGUAGE' not in st.session_state:
    st.session_state['SESSION_LANGUAGE'] = util.read_json_at(INIT_LANGUAGE, 'SESSION_LANGUAGE', default_value='en_US')

if 'FILTER_ROW_COUNT' not in st.session_state:
    st.session_state['FILTER_ROW_COUNT'] = util.read_json_at(BRAIN_MEMO, 'filter_row_count', default_value=1)

# models
MODELS_OPTIONS = ['gpt-3.5-turbo', 'text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001']

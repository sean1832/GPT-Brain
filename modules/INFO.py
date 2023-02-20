import streamlit as st
import time
import modules.utilities as util

st.set_page_config(
    page_title='GPT Brain'
)

# path
USER_DIR = '.user'
LOG_PATH = '.user/log'
BRAIN_MEMO = '.user/brain-memo.json'
MANIFEST = '.core/manifest.json'
INIT_LANGUAGE = '.user/language.json'

# activate session
if 'SESSION_TIME' not in st.session_state:
    st.session_state['SESSION_TIME'] = time.strftime("%Y%m%d-%H%H%S")

if 'SESSION_LANGUAGE' not in st.session_state:
    st.session_state['SESSION_LANGUAGE'] = util.read_json_at(INIT_LANGUAGE, 'SESSION_LANGUAGE')

if 'FILTER_ROW_COUNT' not in st.session_state:
    st.session_state['FILTER_ROW_COUNT'] = util.read_json_at(BRAIN_MEMO, 'filter_row_count')

SESSION_TIME = st.session_state['SESSION_TIME']

CURRENT_LOG_FILE = f'{LOG_PATH}/log_{SESSION_TIME}.log'

# models
MODELS_OPTIONS = ['text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001']

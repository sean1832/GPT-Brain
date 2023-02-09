import streamlit as st
from modules import utilities as util
import initial_file_creator
import brain
import check_update
import time
import os

# activate session
if 'SESSION_TIME' not in st.session_state:
    st.session_state['SESSION_TIME'] = time.strftime("%Y%m%d-%H%H%S")

st.set_page_config(
    page_title='Seanium Brain'
)



model_options = ['text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001']
header = st.container()
body = st.container()
LOG_PATH = '.user/log'
SESSION_TIME = st.session_state['SESSION_TIME']
CURRENT_LOG_FILE = f'{LOG_PATH}/log_{SESSION_TIME}.log'




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
    for root, dirs, files in os.walk(LOG_PATH):
        for file in files:
            if not file == log_file_name:
                os.remove(os.path.join(root, file))


def save_as():
    # download log file
    with open(CURRENT_LOG_FILE, 'rb') as f:
        content = f.read()
        st.download_button(
            label="📥download log",
            data=content,
            file_name=f'log_{SESSION_TIME}.txt',
            mime='text/plain'
        )


# sidebar
with st.sidebar:
    st.title('Settings')
    output_types = st.multiselect('Output Types', ['Answer', 'Summary'], default=['Answer'])
    answer_model = st.selectbox('Answer Model', model_options)
    if util.contains(output_types, 'Summary'):
        summary_model = st.selectbox('Summary Model', model_options)

    temp = st.slider('Temperature', 0.0, 1.0, value=0.1)
    max_tokens = st.slider('Max Tokens', 850, 2500, value=1000)
    top_p = st.slider('Top_P', 0.0, 1.0, value=1.0)
    freq_panl = st.slider('Frequency penalty', 0.0, 1.0, value=0.0)
    pres_panl = st.slider('Presence penalty', 0.0, 1.0, value=0.0)

    chunk_size = st.slider('Chunk Size', 1500, 4500, value=4000)
    chunk_count = st.slider('Answer Count', 1, 5, value=1)

    if st.button('Clear Log', on_click=clear_log):
        st.success('Log Cleared')
with header:
    st.title('🧠Seanium Brain')
    st.text('This is my personal AI powered brain feeding my own Obsidian notes. Ask anything.')


def execute_brain(q):
    # log question
    log(f'\n\n\n\n[{str(time.ctime())}] - QUESTION: {q}')

    if check_update.isUpdated():
        # if brain-info is updated
        brain.build(chunk_size)
        st.success('Brain rebuild!')
        time.sleep(2)

    # thinking on answer
    with st.spinner('Thinking on Answer'):
        answer = brain.run_answer(q, answer_model, temp, max_tokens, top_p, freq_panl, pres_panl,
                                  chunk_count=chunk_count)
        if util.contains(output_types, 'Answer'):
            # displaying results
            st.header('💬Answer')
            st.success(answer)
            log(answer, delimiter='ANSWER')

    # thinking on summary
    if util.contains(output_types, 'Summary'):
        with st.spinner('Thinking on Summary'):
            time.sleep(2)
            summary = brain.run_summary(answer, summary_model, temp, max_tokens, top_p, freq_panl, pres_panl)
            # displaying results
            st.header('📃Summary')
            st.success(summary)
            log(summary, delimiter='SUMMARY')


# main
with body:
    question = st.text_input('Ask Brain: ')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        send = st.button('📩Send')
    with col2:
        if os.path.exists(CURRENT_LOG_FILE):
            save_as()

    # execute brain calculation
    if not question == '' and send:
        execute_brain(question)

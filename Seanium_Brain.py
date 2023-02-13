import streamlit as st
from modules import utilities as util
from modules import model_data
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

util.remove_oldest_file('.user/log', 10)

model_options = ['text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001']
header = st.container()
body = st.container()
LOG_PATH = '.user/log'
PROMPT_PATH = '.user/prompt'
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


def process_response(query, target_model, prompt_file: str, data: model_data.param):
    # check if exclude model is not target model
    file_name = util.get_file_name(prompt_file)
    print(f'Processing {file_name}...')
    with st.spinner(f'Thinking on {file_name}...'):
        results = brain.run(query, target_model, prompt_file,
                            data.temp,
                            data.max_tokens,
                            data.top_p,
                            data.frequency_penalty,
                            data.present_penalty)
        # displaying results
        st.header(f'📃{file_name}')
        st.success(results)
        time.sleep(1)
        log(results, delimiter=f'{file_name.upper()}')


# sidebar
with st.sidebar:
    st.title('Settings')

    prompt_files = util.scan_directory(PROMPT_PATH)
    prompt_file_names = [util.get_file_name(file) for file in prompt_files]
    prompt_dictionary = dict(zip(prompt_file_names, prompt_files))
    # remove 'my-info' from prompt dictionary
    prompt_dictionary.pop('my-info')

    operations = st.multiselect('Operations', list(prompt_dictionary.keys()), default=list(prompt_dictionary.keys())[0])
    other_models = []
    question_model = st.selectbox('Question Model', model_options)

    operations_no_question = [op for op in operations if op != 'question']

    for operation in operations_no_question:
        model = st.selectbox(f'{operation} Model', model_options)
        other_models.append(model)

    temp = st.slider('Temperature', 0.0, 1.0, value=0.1)
    max_tokens = st.slider('Max Tokens', 850, 4500, value=1000)
    top_p = st.slider('Top_P', 0.0, 1.0, value=1.0)
    freq_panl = st.slider('Frequency penalty', 0.0, 1.0, value=0.0)
    pres_panl = st.slider('Presence penalty', 0.0, 1.0, value=0.0)

    chunk_size = st.slider('Chunk Size', 1500, 4500, value=4000)
    chunk_count = st.slider('Answer Count', 1, 5, value=1)

    param = model_data.param(temp=temp,
                             max_tokens=max_tokens,
                             top_p=top_p,
                             frequency_penalty=freq_panl,
                             present_penalty=pres_panl,
                             chunk_size=chunk_size,
                             chunk_count=chunk_count)

    if st.button('Clear Log', on_click=clear_log):
        st.success('Log Cleared')
with header:
    st.title('🧠Seanium Brain')
    st.text('This is my personal AI powered brain feeding my own Obsidian notes. Ask anything.')


def execute_brain(q):
    # log question
    log(f'\n\n\n\n[{str(time.ctime())}] - QUESTION: {q}')

    if check_update.isUpdated():
        st.success('Building Brain...')
        # if brain-info is updated
        brain.build(chunk_size)
        st.success('Brain rebuild!')
        time.sleep(2)

    # thinking on answer
    with st.spinner('Thinking on Answer'):
        answer = brain.run_answer(q, question_model, temp, max_tokens, top_p, freq_panl, pres_panl,
                                  chunk_count=chunk_count)
        if util.contains(operations, 'question'):
            # displaying results
            st.header('💬Answer')
            st.success(answer)
            time.sleep(1)
            log(answer, delimiter='ANSWER')

    # thinking on other outputs
    if len(operations_no_question) > 0:
        for i in range(len(operations_no_question)):
            prompt_path = prompt_dictionary[operations_no_question[i]]
            other_model = other_models[i]
            process_response(answer, other_model, prompt_path, param)


# main
with body:
    question = st.text_area('Ask Brain: ')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        send = st.button('📩Send')
    with col2:
        if os.path.exists(CURRENT_LOG_FILE):
            save_as()

    # execute brain calculation
    if not question == '' and send:
        execute_brain(question)

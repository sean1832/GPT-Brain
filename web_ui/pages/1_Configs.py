import streamlit as st
import os
from modules import utilities as util
import tkinter as tk
from tkinter import filedialog

st.set_page_config(
    page_title='Configs'
)

body = st.container()

user_dir = '.user/'
prompt_dir = f'{user_dir}prompt/'
brain_memo = f'{user_dir}brain-memo.json'


def save(content, path, page=''):
    save_but = st.button('💾Save')
    if save_but:
        util.write_file(content, path)
        st.success(f'✅File saved!')
        # write to json file
        if page == '💽Brain Memory':
            util.update_json(brain_memo, 'delimiter', delimiter)
            util.update_json(brain_memo, 'append_mode', append_mode)
            util.update_json(brain_memo, 'force_mode', force_delimiter)


def select_directory():
    root = tk.Tk()
    root.withdraw()
    # make sure the dialog is on top of the main window
    root.attributes('-topmost', True)
    directory = filedialog.askdirectory(initialdir=os.getcwd(), title='Select Note Directory', master=root)
    return directory


with st.sidebar:
    st.title('Settings')
    menu = st.radio('Menu', [
        '📝Prompts',
        '💽Brain Memory',
        '🔑API Keys'
    ])

with body:
    match menu:
        case '📝Prompts':
            st.title('📝Prompts')
            st.text('Configuration of prompts.')
            selected_file = st.selectbox('Prompt File', os.listdir(prompt_dir))
            selected_path = prompt_dir + selected_file
            mod_text = st.text_area('Prompts', value=util.read_file(selected_path), height=500)
            save(mod_text, selected_path)

        case '💽Brain Memory':
            st.title('💽Brain Memory')
            st.text('Modify your brain knowledge base.')
            memory_data = util.read_file(f'{user_dir}input.txt')

            note_dir = ''

            col1, col2 = st.columns(2)
            with col1:
                st.button('🔄Refresh')
            with col2:
                if st.button('📁Select Note Directory'):
                    note_dir = select_directory()
                    util.update_json(brain_memo, 'note_dir', note_dir)
            note_dir = st.text_input('Note Directory', value=util.read_json_at(brain_memo, 'note_dir'),
                                     placeholder='Select Note Directory', key='note_dir')

            col1, col2 = st.columns(2)
            with col1:
                delimiter_memo = util.read_json_at(brain_memo, 'delimiter')
                delimiter = st.text_input('Delimiter', delimiter_memo, placeholder='e.g. +++')

            with col2:
                append_mode = st.checkbox('Append Mode', value=util.read_json_at(brain_memo, 'append_mode'))

                force_delimiter = st.checkbox('Force Delimiter', value=util.read_json_at(brain_memo, 'force_mode'))

            # if note directory is selected
            if note_dir != '':

                note_data = util.read_files(note_dir, delimiter, force_delimiter)
                if append_mode:
                    memory_data += note_data
                else:
                    memory_data = note_data

            mod_text = st.text_area('Raw Memory Inputs', value=memory_data, height=500)
            save(mod_text, f'{user_dir}input.txt', '💽Brain Memory')

        case '🔑API Keys':
            st.title('🔑API Keys')
            st.text('Configure your OpenAI API keys.')
            mod_text = st.text_input('API Keys', value=util.read_file(f'{user_dir}API-KEYS.txt'))
            save(mod_text, f'{user_dir}API-KEYS.txt')

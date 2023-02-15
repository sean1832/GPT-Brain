import time

import streamlit as st
import streamlit_toggle as st_toggle

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


def save(content, path, page='', json_value: dict = None):
    if json_value is None:
        json_value = []
    save_but = st.button('💾Save')
    if save_but:
        util.write_file(content, path)
        st.success(f'✅File saved!')
        # write to json file
        if page == '💽Brain Memory':
            util.update_json(brain_memo, 'delimiter', json_value['delimiter'])
            util.update_json(brain_memo, 'append_mode', json_value['append_mode'])
            util.update_json(brain_memo, 'force_mode', json_value['force_mode'])
            util.update_json(brain_memo, 'advanced_mode', json_value['advanced_mode'])
            util.update_json(brain_memo, 'filter_keys', json_value['filter_keys'])
            util.update_json(brain_memo, 'filter_logics', json_value['filter_logics'])
            util.update_json(brain_memo, 'filter_values', json_value['filter_values'])
        time.sleep(1)
        # refresh page
        st.experimental_rerun()


def select_directory():
    root = tk.Tk()
    root.withdraw()
    # make sure the dialog is on top of the main window
    root.attributes('-topmost', True)
    directory = filedialog.askdirectory(initialdir=os.getcwd(), title='Select Note Directory', master=root)
    return directory


def match_logic(logic, filter_key, filter_val, key, value):
    key_match = filter_key == key
    if logic == 'IS':
        return key_match and filter_val == value
    elif logic == 'IS NOT':
        return key_match and filter_val != value
    elif logic == 'CONTAINS':
        return key_match and filter_val in value
    elif logic == 'NOT CONTAINS':
        return key_match and filter_val not in value
    elif logic == 'MORE THAN':
        # check if value is float
        if not value.isnumeric():
            return False
        return key_match and float(filter_val) < float(value)
    elif logic == 'LESS THAN':
        # check if value is float
        if not value.isnumeric():
            return False
        return key_match and float(filter_val) > float(value)
    elif logic == 'MORE THAN OR EQUAL':
        # check if value is float
        if not value.isnumeric():
            return False
        return key_match and float(filter_val) <= float(value)
    elif logic == 'LESS THAN OR EQUAL':
        # check if value is float
        if not value.isnumeric():
            return False
        return key_match and float(filter_val) >= float(value)
    else:
        return False


def extract_frontmatter(content, delimiter='---'):
    # extract metadata
    try:
        yaml = util.extract_string(content, delimiter, True, join=False, split_mode=True)[1]
    except IndexError:
        yaml = ''
    fields = yaml.split('\n')
    return fields


def match_fields(contents: list, logic_select, filter_key, filter_val):
    filtered_contents = []
    for content in contents:
        fields = extract_frontmatter(content, delimiter='---')
        for field in fields:
            if field == '':
                continue
            key, value = field.split(':')
            key = key.strip()
            value = value.strip()
            if match_logic(logic_select, filter_key, filter_val, key, value):
                filtered_contents.append(content)
                break
    return filtered_contents


def add_filter(num):
    # filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_key = st.text_input(f'Key{num}', placeholder='Key', value=util.read_json_at(brain_memo, 'filter_keys'))
    with col2:
        options = ['IS',
                   'IS NOT',
                   'CONTAINS',
                   'NOT CONTAINS',
                   'MORE THAN',
                   'LESS THAN',
                   'MORE THAN OR EQUAL',
                   'LESS THAN OR EQUAL']
        default_index = util.get_index(options, 'filter_logics', 0)
        logic_select = st.selectbox(f'Logic{num}', options, index=default_index)
    with col3:
        value = util.read_json_at(brain_memo, 'filter_values')
        if isinstance(value, int):
            value = "{:02}".format(value)
        filter_val = st.text_input(f'value{num}', placeholder='Value', value=value)
    return filter_key, logic_select, filter_val


def filter_data(contents: list, append=True):

    # add filter
    filter_key, logic_select, filter_val = add_filter(0)

    # filter data
    filtered_contents = match_fields(contents, logic_select, filter_key, filter_val)
    result = filtered_contents
    if append:
        return '\n\n\n\n'.join(result), filter_key, logic_select, filter_val
    else:
        return result, filter_key, logic_select, filter_val


def main():
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

                # read selected file
                last_sel_file = util.read_json_at(brain_memo, 'selected_prompt')
                all_files = os.listdir(prompt_dir)
                # sort files base on creation time
                all_files.sort(key=lambda x: os.path.getmtime(f'{prompt_dir}{x}'), reverse=True)

                # index of last selected file
                try:
                    last_sel_file_index = all_files.index(last_sel_file)
                except ValueError:
                    last_sel_file_index = 0

                selected_file = st.selectbox('Prompt File', all_files, last_sel_file_index)

                col1, col2 = st.columns(2)
                with col1:
                    if st_toggle.st_toggle_switch('New Prompt', label_after=True):
                        new_file = st.text_input('New Prompt Name', value='new_prompt')
                        if st.button('Create'):
                            util.write_file('', f'{prompt_dir}{new_file}.txt')
                            # change select file to new fie
                            util.update_json(brain_memo, 'selected_prompt', selected_file)
                            # refresh page
                            st.experimental_rerun()
                with col2:
                    is_core = selected_file == 'my-info.txt' or \
                              selected_file == 'question.txt' or \
                              selected_file == 'summarize.txt'
                    if not is_core:
                        if st_toggle.st_toggle_switch('Delete Prompt', label_after=True):
                            if st.button('❌Delete'):
                                util.delete_file(f'{prompt_dir}{selected_file}')
                                # refresh page
                                st.experimental_rerun()

                selected_path = prompt_dir + selected_file
                mod_text = st.text_area('Prompts', value=util.read_file(selected_path), height=500)
                save(mod_text, selected_path)

            case '💽Brain Memory':
                st.title('💽Brain Memory')
                st.text('Modify your brain knowledge base.')
                memory_data = util.read_file(f'{user_dir}input.txt')

                col1, col2 = st.columns(2)
                with col1:
                    st.button('🔄Refresh')
                with col2:
                    if st.button('📁Select Note Directory'):
                        note_dir = select_directory()
                        util.update_json(brain_memo, 'note_dir', note_dir)
                note_dir = st.text_input('Note Directory', value=util.read_json_at(brain_memo, 'note_dir'),
                                         placeholder='Select Note Directory', key='note_dir')

                col1, col2, col3 = st.columns(3)
                with col1:
                    delimiter_memo = util.read_json_at(brain_memo, 'delimiter')
                    delimiter = st.text_input('Delimiter', delimiter_memo, placeholder='e.g. +++')

                with col2:
                    append_mode = st.checkbox('Append Mode', value=util.read_json_at(brain_memo, 'append_mode'))
                    force_delimiter = st.checkbox('Force Delimiter', value=util.read_json_at(brain_memo, 'force_mode'))
                with col3:
                    advanced_mode = st_toggle.st_toggle_switch('Filter Mode',
                                                               label_after=True,
                                                               default_value=util.read_json_at(brain_memo,
                                                                                               'advanced_mode', False))

                filter_key = ''
                filter_logic = 'IS'
                filter_val = ''

                # if note directory is selected
                if note_dir != '':
                    # if advanced mode enabled
                    if advanced_mode:
                        note_datas = util.read_files(note_dir, single_string=False)
                        note_datas, filter_key, filter_logic, filter_val = filter_data(note_datas, True)
                        modified_data = util.parse_data(note_datas, delimiter, force_delimiter)
                    else:
                        modified_data = util.read_files(note_dir, single_string=True, delimiter=delimiter,
                                                        force=force_delimiter)
                    if append_mode:
                        memory_data += modified_data
                    else:
                        memory_data = modified_data

                mod_text = st.text_area('Raw Memory Inputs', value=memory_data, height=500)
                save(mod_text, f'{user_dir}input.txt', '💽Brain Memory', {
                    'delimiter': delimiter,
                    'append_mode': append_mode,
                    'force_mode': force_delimiter,
                    'advanced_mode': advanced_mode,
                    'filter_keys': filter_key,
                    'filter_logics': filter_logic,
                    'filter_values': filter_val
                })

            case '🔑API Keys':
                st.title('🔑API Keys')
                st.text('Configure your OpenAI API keys.')
                mod_text = st.text_input('API Keys', value=util.read_file(f'{user_dir}API-KEYS.txt'))
                save(mod_text, f'{user_dir}API-KEYS.txt')


if __name__ == '__main__':
    main()

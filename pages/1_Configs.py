import time

import streamlit as st
import streamlit_toggle as st_toggle

import os
from modules import utilities as util
import tkinter as tk
from tkinter import filedialog
from modules import language

user_dir = '.user/'
prompt_dir = f'{user_dir}prompt/'
brain_memo = f'{user_dir}brain-memo.json'

if 'FILTER_ROW_COUNT' not in st.session_state:
    st.session_state['FILTER_ROW_COUNT'] = util.read_json_at(brain_memo, 'filter_row_count')

_ = language.set_language()

st.set_page_config(
    page_title='Configs'
)

body = st.container()


def save(content, path, page='', json_value: dict = None):
    if json_value is None:
        json_value = []
    save_but = st.button(_('💾Save'))
    if save_but:
        util.write_file(content, path)
        st.success(_('✅File saved!'))
        # write to json file
        if page == '💽Brain Memory':
            util.update_json(brain_memo, 'delimiter', json_value['delimiter'])
            util.update_json(brain_memo, 'append_mode', json_value['append_mode'])
            util.update_json(brain_memo, 'force_mode', json_value['force_mode'])
            util.update_json(brain_memo, 'advanced_mode', json_value['advanced_mode'])
            util.update_json(brain_memo, 'filter_info', json_value['filter_info'])
            util.update_json(brain_memo, 'filter_row_count', json_value['filter_row_count'])
        time.sleep(1)
        # refresh page
        st.experimental_rerun()


def select_directory():
    root = tk.Tk()
    root.withdraw()
    # make sure the dialog is on top of the main window
    root.attributes('-topmost', True)
    directory = filedialog.askdirectory(initialdir=os.getcwd(), title=_('Select Note Directory'), master=root)
    return directory


def match_logic(operator, filter_val, value):
    if operator == 'IS':
        return filter_val == value
    elif operator == 'IS NOT':
        return filter_val != value
    elif operator == 'CONTAINS':
        return filter_val in value
    elif operator == 'NOT CONTAINS':
        return filter_val not in value
    elif operator == 'MORE THAN':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) < float(value)
    elif operator == 'LESS THAN':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) > float(value)
    elif operator == 'MORE THAN OR EQUAL':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) <= float(value)
    elif operator == 'LESS THAN OR EQUAL':
        # check if value is float
        if not value.isnumeric():
            return False
        return float(filter_val) >= float(value)
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


def match_fields(pages: list, filter_datas: list[dict]):
    filtered_contents = []
    for page in pages:
        fields = extract_frontmatter(page, delimiter='---')

        found_data = []

        for field in fields:
            if field == '':
                continue
            found_key, found_value = field.split(':')
            found_key = found_key.strip()
            found_value = found_value.strip()

            found_data.append({
                'key': found_key,
                'value': found_value
            })

        found_match = []
        for data in filter_datas:
            for found in found_data:
                data_key = data['key'].lower()
                data_val = data['value'].lower()
                found_key = found['key'].lower()
                found_val = found['value'].lower()
                if data_key == found_key:
                    if match_logic(data['logic'], data_val, found_val):
                        # found single match
                        found_match.append(True)

        # if all match
        if found_match.count(True) == len(filter_datas):
            filtered_contents.append(page)

    combined_contents = '\n\n\n\n'.join(filtered_contents)
    return combined_contents


def add_filter(num, val_filter_key, val_filter_logic, val_filter_val):
    # filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_key = st.text_input(f'Key{num}', placeholder='Key', value=val_filter_key)
    with col2:
        options = ['CONTAINS',
                   'NOT CONTAINS',
                   'IS',
                   'IS NOT',
                   'MORE THAN',
                   'LESS THAN',
                   'MORE THAN OR EQUAL',
                   'LESS THAN OR EQUAL']
        default_index = util.get_index(options, val_filter_logic, 0)
        logic_select = st.selectbox(f'Logic{num}', options, index=default_index)
    with col3:
        if isinstance(val_filter_val, int):
            val_filter_val = "{:02}".format(val_filter_val)
        filter_val = st.text_input(f'value{num}', placeholder='Value', value=val_filter_val)
    return filter_key, logic_select, filter_val


def filter_data(pages: list, add_filter_button, del_filter_button):
    init_filter_infos = util.read_json_at(brain_memo, 'filter_info')

    filter_datas = []
    if add_filter_button:
        st.session_state['FILTER_ROW_COUNT'] += 1
    if del_filter_button:
        st.session_state['FILTER_ROW_COUNT'] -= 1
    if st.session_state['FILTER_ROW_COUNT'] >= 1:
        for i in range(st.session_state['FILTER_ROW_COUNT'] + 1):
            try:
                init_info = init_filter_infos[i - 1]
                init_key = init_info['key']
                init_logic = init_info['logic']
                init_val = init_info['value']
            except IndexError:
                init_key = ''
                init_logic = 'CONTAINS'
                init_val = ''

            if i == 0:
                continue
            # add filter
            filter_key, logic_select, filter_val = add_filter(i, init_key, init_logic, init_val)
            data = {'key': filter_key, 'logic': logic_select, 'value': filter_val}
            filter_datas.append(data)

    # filter data
    filtered_contents = match_fields(pages, filter_datas)
    return filtered_contents, filter_datas


def main():
    with st.sidebar:
        st.title(_('Settings'))
        menu = st.radio(_('Menu'), [
            _('📝Prompts'),
            _('💽Brain Memory'),
            _('🔑API Keys')
        ])

    with body:
        match menu:
            case _('📝Prompts'):
                st.title(_('📝Prompts'))
                st.text(_('Configuration of prompts.'))

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

                selected_file = st.selectbox(_('Prompt File'), all_files, last_sel_file_index)

                col1, col2 = st.columns(2)
                with col1:
                    if st_toggle.st_toggle_switch(_('New Prompt'), label_after=True):
                        new_file = st.text_input(_('New Prompt Name'), value='new_prompt')
                        if st.button(_('Create')):
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
                        if st_toggle.st_toggle_switch(_('Delete Prompt'), label_after=True):
                            if st.button(_('❌Delete')):
                                util.delete_file(f'{prompt_dir}{selected_file}')
                                # refresh page
                                st.experimental_rerun()

                selected_path = prompt_dir + selected_file
                mod_text = st.text_area(_('Prompts'), value=util.read_file(selected_path), height=500)
                save(mod_text, selected_path)

            case _('💽Brain Memory'):
                st.title(_('💽Brain Memory'))
                st.text(_('Modify your brain knowledge base.'))
                memory_data = util.read_file(f'{user_dir}input.txt')

                col1, col2 = st.columns(2)
                with col1:
                    st.button(_('🔄Refresh'))
                with col2:
                    if st.button(_('📁Select Note Directory')):
                        note_dir = select_directory()
                        util.update_json(brain_memo, 'note_dir', note_dir)
                note_dir = st.text_input(_('Note Directory'), value=util.read_json_at(brain_memo, 'note_dir'),
                                         placeholder=_('Select Note Directory'), key='note_dir')

                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                with col1:
                    delimiter_memo = util.read_json_at(brain_memo, 'delimiter')
                    delimiter = st.text_input(_('Delimiter'), delimiter_memo, placeholder='e.g. +++')

                with col2:
                    append_mode = st.checkbox(_('Append Mode'), value=util.read_json_at(brain_memo, 'append_mode'))
                    force_delimiter = st.checkbox(_('Force Delimiter'),
                                                  value=util.read_json_at(brain_memo, 'force_mode'))
                with col3:
                    advanced_mode = st_toggle.st_toggle_switch(_('Filter Mode'),
                                                               label_after=True,
                                                               default_value=util.read_json_at(brain_memo,
                                                                                               'advanced_mode', False))
                with col4:
                    if advanced_mode:
                        add_filter_button = st.button(_('Add Filter'))
                        del_filter_button = st.button(_('Delete Filter'))

                # if note directory is selected
                if note_dir != '':
                    # if advanced mode enabled
                    if advanced_mode:
                        note_datas = util.read_files(note_dir, single_string=False)
                        note_datas, filter_info = filter_data(note_datas, add_filter_button, del_filter_button)
                        # note_datas, filter_key, filter_logic, filter_val = filter_data(note_datas, True)
                        modified_data = util.parse_data(note_datas, delimiter, force_delimiter)
                    else:
                        modified_data = util.read_files(note_dir, single_string=True, delimiter=delimiter,
                                                        force=force_delimiter)
                    if append_mode:
                        memory_data += modified_data
                    else:
                        memory_data = modified_data

                mod_text = st.text_area(_('Raw Memory Inputs'), value=memory_data, height=500)
                save(mod_text, f'{user_dir}input.txt', _('💽Brain Memory'), {
                    'delimiter': delimiter,
                    'append_mode': append_mode,
                    'force_mode': force_delimiter,
                    'advanced_mode': advanced_mode,
                    'filter_info': filter_info,
                    'filter_row_count': len(filter_info),
                })

            case _('🔑API Keys'):
                st.title(_('🔑API Keys'))
                st.text(_('Configure your OpenAI API keys.'))
                mod_text = st.text_input(_('API Keys'), value=util.read_file(f'{user_dir}API-KEYS.txt'))
                save(mod_text, f'{user_dir}API-KEYS.txt')


if __name__ == '__main__':
    main()

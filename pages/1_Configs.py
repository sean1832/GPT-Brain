import os

import streamlit as st
import streamlit_toggle as st_toggle

import modules.language as language
import modules.utilities as util
import modules.INFO as INFO
import streamlit_toolkit.tools as st_tools

SESSION_LANG = st.session_state['SESSION_LANGUAGE']
PROMPT_PATH = f'{INFO.USER_DIR}/prompt/{SESSION_LANG}/'

_ = language.set_language()

# st.set_page_config(
#     page_title='Configs'
# )

body = st.container()


def main():
    with st.sidebar:
        st.title(_('Settings'))
        menu = st.radio(_('Menu'), [
            _('📝Prompts'),
            _('💽Brain Memory'),
            _('🔑API Keys')
        ])

    with body:
        if menu == _('📝Prompts'):
            st.title(_('📝Prompts'))
            st.text(_('Configuration of prompts.'))

            # read selected file
            last_sel_file = util.read_json_at(INFO.BRAIN_MEMO, 'selected_prompt')
            all_files = os.listdir(PROMPT_PATH)
            # sort files base on creation time
            all_files.sort(key=lambda x: os.path.getmtime(f'{PROMPT_PATH}{x}'), reverse=True)

            # index of last selected file
            try:
                last_sel_file_index = all_files.index(last_sel_file)
            except ValueError:
                last_sel_file_index = 0

            selected_file = st.selectbox(_('Prompt File'), all_files, last_sel_file_index)

            col1, col2 = st.columns(2)
            with col1:
                if st_toggle.st_toggle_switch(_('New Prompt'), label_after=True):
                    new_file = st.text_input(_('New Prompt Name'), value=_('new_prompt'))
                    if st.button(_('Create')):
                        util.write_file('', f'{PROMPT_PATH}{new_file}.txt')
                        # change select file to new fie
                        util.update_json(INFO.BRAIN_MEMO, 'selected_prompt', selected_file)
                        # refresh page
                        st.experimental_rerun()
            with col2:
                is_core = selected_file == _('my-info') + '.txt' or \
                          selected_file == _('question') + '.txt' or \
                          selected_file == _('summarize') + '.txt'
                if not is_core:
                    if st_toggle.st_toggle_switch(_('Delete Prompt'), label_after=True):
                        if st.button(_('❌Delete')):
                            util.delete_file(f'{PROMPT_PATH}{selected_file}')
                            # refresh page
                            st.experimental_rerun()

            selected_path = PROMPT_PATH + selected_file
            mod_text = st.text_area(_('Prompts'), value=util.read_file(selected_path), height=500)
            st_tools.save(mod_text, selected_path)

        if menu == _('💽Brain Memory'):
            st.title(_('💽Brain Memory'))
            st.text(_('Modify your brain knowledge base.'))
            memory_data = util.read_file(f'{INFO.USER_DIR}/input.txt')

            col1, col2 = st.columns(2)
            with col1:
                st.button(_('🔄Refresh'))
            with col2:
                if st.button(_('📁Select Note Directory')):
                    note_dir = st_tools.select_directory(util.read_json_at(INFO.BRAIN_MEMO, 'note_dir'))
                    util.update_json(INFO.BRAIN_MEMO, 'note_dir', note_dir)
            note_dir = st.text_input(_('Note Directory'), value=util.read_json_at(INFO.BRAIN_MEMO, 'note_dir'),
                                     placeholder=_('Select Note Directory'), key='note_dir')

            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            with col1:
                delimiter_memo = util.read_json_at(INFO.BRAIN_MEMO, 'delimiter')
                delimiter = st.text_input(_('Delimiter'), delimiter_memo, placeholder='e.g. +++')

            with col2:
                append_mode = st.checkbox(_('Append Mode'), value=util.read_json_at(INFO.BRAIN_MEMO, 'append_mode'))
                force_delimiter = st.checkbox(_('Force Delimiter'),
                                              value=util.read_json_at(INFO.BRAIN_MEMO, 'force_mode'))
            with col3:
                advanced_mode = st_toggle.st_toggle_switch(_('Filter Mode'),
                                                           label_after=True,
                                                           default_value=util.read_json_at(INFO.BRAIN_MEMO,
                                                                                           'advanced_mode', False))
            with col4:
                if advanced_mode:
                    add_filter_button = st.button("➕" + _('Add Filter'))
                    del_filter_button = st.button("❌" + _('Delete Filter'))

            filter_info = {}
            # if note directory is selected
            if note_dir != '':

                # if advanced mode enabled
                if advanced_mode:
                    note_datas = util.read_files(note_dir, single_string=False, exclude_dir=INFO.EXCLUDE_DIR)
                    note_datas, filter_info = st_tools.filter_data(note_datas, add_filter_button, del_filter_button)
                    # note_datas, filter_key, filter_logic, filter_val = filter_data(note_datas, True)
                    modified_data = util.parse_data(note_datas, delimiter, force_delimiter)
                else:
                    modified_data = util.read_files(note_dir, single_string=True, delimiter=delimiter,
                                                    force=force_delimiter, exclude_dir=INFO.EXCLUDE_DIR)

                # append mode
                if append_mode:
                    memory_data += modified_data
                else:
                    memory_data = modified_data

            mod_text = st.text_area(_('Raw Memory Inputs'), value=memory_data, height=500)
            st_tools.save(mod_text, f'{INFO.USER_DIR}/input.txt', _('💽Brain Memory'), {
                'delimiter': delimiter,
                'append_mode': append_mode,
                'force_mode': force_delimiter,
                'advanced_mode': advanced_mode,
                'filter_info': filter_info,
                'filter_row_count': len(filter_info),
            })

        if menu == _('🔑API Keys'):
            st.title(_('🔑API Keys'))
            st.text(_('Configure your OpenAI API keys.'))
            mod_text = st.text_input(_('API Keys'), value=util.read_file(f'{INFO.USER_DIR}/API-KEYS.txt'))
            st_tools.save(mod_text, f'{INFO.USER_DIR}/API-KEYS.txt')


if __name__ == '__main__':
    main()

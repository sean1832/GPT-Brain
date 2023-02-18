import gettext
import streamlit as st
import modules.utilities as util

languages = util.read_json('.locals/languages.json')


def select_language():
    language_index = util.get_index(list(languages.values()), st.session_state['SESSION_LANGUAGE'])

    # Add a language selector widget to the Streamlit app
    language = st.sidebar.selectbox('Language', languages.keys(), language_index)

    selected_lang = languages[language]

    if st.session_state['SESSION_LANGUAGE'] != selected_lang:
        st.session_state['SESSION_LANGUAGE'] = selected_lang
        util.write_json({'SESSION_LANGUAGE': selected_lang}, '.user/language.json')
        st.experimental_rerun()


def set_language():
    # set current language
    lang_translations = gettext.translation('base', localedir='.locals', languages=[st.session_state['SESSION_LANGUAGE']])
    lang_translations.install()
    # define _ shortcut for translations
    _ = lang_translations.gettext
    return _

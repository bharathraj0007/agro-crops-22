import json
import os
import streamlit as st

def load_translations():
    translations = {}
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
    
    for filename in os.listdir(locales_dir):
        if filename.endswith('.json'):
            lang = filename.split('.')[0]
            with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                translations[lang] = json.load(f)
    
    return translations

translations = load_translations()

def get_text(key, lang=None):
    """Get translated text for the specified language or current session language"""
    if lang is None:
        lang = st.session_state.get('lang', 'en')
    return translations.get(lang, {}).get(key, key)

def set_language(lang):
    """Set the current language in session state"""
    st.session_state.lang = lang

def get_language_switcher():
    """Render the language switcher component"""
    # Ensure language is set in session state
    if 'lang' not in st.session_state:
        st.session_state.lang = 'en'
    
    # Language selector (DO NOT wrap in st.sidebar here - will be called from app.py within sidebar)
    st.markdown("### " + get_text("language"))
    
    # Language selection radio button
    current_index = 0 if st.session_state.lang == 'en' else 1
    lang_option = st.radio(
        get_text("select_language"),
        ["English", "ಕನ್ನಡ"],
        index=current_index,
        key="lang_radio"
    )
    
    # Update language when apply is clicked
    if st.button(get_text("apply"), key="lang_apply", use_container_width=True):
        new_lang = 'en' if lang_option == "English" else 'kn'
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()
    
    # Show current language
    st.markdown(f"*{get_text('current_language')}: {lang_option}*")
    st.markdown("---")
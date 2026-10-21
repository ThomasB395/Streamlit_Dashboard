import json, os
import streamlit as st

TRANSLATIONS_FILE = os.path.join(os.path.dirname(__file__), "translations.json")
# The English translations are pre-computed and stored in this file (French text -> English text).
# The app only reads it: no translation model, no download, the result is the same on every computer (deterministic).


@st.cache_data
def _load():
    with open(TRANSLATIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def tr(text):
    # Return the text unchanged in French, or translated in English if the user selected EN in the sidebar.
    if not isinstance(text, str) or not text.strip() or st.session_state.get("lang", "fr") == "fr":
        return text
    return _load().get(text, text)   # If a text is not in the file (ex: dynamic text with numbers), it is displayed as it is.

import json, os
import streamlit as st
import argostranslate.package
import argostranslate.translate

CACHE_FILE = os.path.join(os.path.dirname(__file__), "translations.json")
# The translations are saved on disk: each text is translated only one time, even after a restart of the app.


def _load():
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


@st.cache_resource(show_spinner="Téléchargement du modèle de traduction (uniquement la première fois)...")
def _model():
    # Install the French -> English model if it is not already installed (download of ~100 MB, one time).
    if not any(l.code == "fr" for l in argostranslate.translate.get_installed_languages()):
        argostranslate.package.update_package_index()
        pkg = next(p for p in argostranslate.package.get_available_packages()
                   if p.from_code == "fr" and p.to_code == "en")
        argostranslate.package.install_from_path(pkg.download())
    langs = {l.code: l for l in argostranslate.translate.get_installed_languages()}
    return langs["fr"].get_translation(langs["en"])


def _translate(text):
    model = _model()
    out = []
    for line in text.split("\n"):   # Line by line to keep the markdown structure (lists, line breaks, indentation).
        core = line.strip()
        if not core:
            out.append(line)
            continue
        indent = line[: len(line) - len(line.lstrip())]
        end = "  " if line.endswith("  ") else ""   # Markdown line break.
        out.append(indent + model.translate(core) + end)
    return "\n".join(out)


def tr(text):
    # Return the text unchanged in French, or translated in English if the user selected EN in the sidebar.
    if not isinstance(text, str) or not text.strip() or st.session_state.get("lang", "fr") == "fr":
        return text
    cache = st.session_state.setdefault("_tr_cache", _load())
    if text in cache:
        return cache[text]
    try:
        cache[text] = _translate(text)
        _save(cache)
        return cache[text]
    except Exception as e:
        if not st.session_state.get("tr_error"):   # We display the error only once.
            st.session_state.tr_error = True
            st.sidebar.error(f"Erreur de traduction : {e}")
        return text

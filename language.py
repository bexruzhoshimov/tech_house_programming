import json
import os

_base = os.path.dirname(os.path.abspath(__file__))
_lang_files = {
    "en": "language/lang_en.json",
    "uz": "language/lang_uz.json"
}
_languages = {}
_current = "en"

def load():
    global _languages
    for code, filename in _lang_files.items():
        path = os.path.join(_base, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                _languages[code] = json.load(f)
        except:
            _languages[code] = {}

def set_language(code):
    global _current
    if code in _languages:
        _current = code

def current():
    return _current

def t(key, **kwargs):
    text = _languages.get(_current, {}).get(key)
    if text is None:
        text = _languages.get("en", {}).get(key, key)
    if not isinstance(text, str):
        text = str(text)
    try:
        return text.format(**kwargs)
    except:
        return text

def value(x):
    if isinstance(x, dict):
        if _current in x:
            return str(x.get(_current))
        if "en" in x:
            return str(x.get("en"))
        for k in x:
            return str(x.get(k))
    return str(x)

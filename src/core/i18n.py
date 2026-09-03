import gettext
import os
from src.core.config import settings

LOCALEDIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')

def get_translator(lang_code: str):
    try:
        t = gettext.translation('messages', localedir=LOCALEDIR, languages=[lang_code])
        return t.gettext
    except FileNotFoundError:
        return gettext.gettext

def _(message: str, lang_code: str = 'fa') -> str:
    return get_translator(lang_code)(message)

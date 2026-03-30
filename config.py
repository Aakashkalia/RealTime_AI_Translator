"""
config.py — Centralized Configuration for Real-Time AI Language Translator
==========================================================================
Contains all supported languages (100+), app constants, and default settings.
Decouples language data from translation/voice modules for clean architecture.
"""

# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION SETTINGS
# ─────────────────────────────────────────────────────────────────────────────

APP_TITLE = "🌍 Real-Time AI Language Translator"
APP_ICON = "🌐"
APP_LAYOUT = "wide"

# Voice settings
VOICE_LISTEN_TIMEOUT = 7        # seconds to wait before giving up
VOICE_PHRASE_TIME_LIMIT = 15    # max seconds of speech per phrase
VOICE_ENERGY_THRESHOLD = 300    # microphone sensitivity threshold

# Translation settings
MAX_CHUNK_SIZE = 4500            # max characters per translation chunk
DEFAULT_SOURCE_LANG = "auto"     # 'auto' means auto-detect
DEFAULT_TARGET_LANG = "hi"       # Hindi as default target

# History settings
HISTORY_FILE = "translation_history.csv"
HISTORY_DISPLAY_LIMIT = 50       # max entries shown in the UI


# ─────────────────────────────────────────────────────────────────────────────
# SUPPORTED LANGUAGES (107 languages — name → ISO 639-1 code)
# ─────────────────────────────────────────────────────────────────────────────
# This dictionary maps human-readable language names to their ISO codes.
# Used by the UI for dropdowns and by the translator/voice modules for API calls.

LANGUAGES = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}

# Reverse lookup: code → name  (used to display detected language)
CODE_TO_LANG = {code: name for name, code in LANGUAGES.items()}

# Sorted language names for dropdown menus
LANGUAGE_NAMES = sorted(LANGUAGES.keys())

# Total count for display
TOTAL_LANGUAGES = len(LANGUAGES)

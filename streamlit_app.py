"""
streamlit_app.py — Main Dashboard for Real-Time AI Language Translator
======================================================================
Premium Streamlit UI with dark glassmorphism theme, voice I/O, 100+ languages,
auto-detection, translation history, and audio playback.

Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
import os

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS — project modules
# ─────────────────────────────────────────────────────────────────────────────
from config import (
    APP_TITLE, APP_ICON, APP_LAYOUT,
    LANGUAGES, LANGUAGE_NAMES, CODE_TO_LANG, TOTAL_LANGUAGES,
)
from translator import translator_handler
from voice_handler import voice_handler
from history_manager import HistoryManager


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Premium dark glassmorphism theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global styles ──────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Gradient header banner ─────────────────────────────────────── */
    .hero-banner {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .hero-banner h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d2ff, #7b2ff7, #ff6ac1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: rgba(255, 255, 255, 0.65);
        font-size: 1.05rem;
        margin-top: 0.6rem;
        font-weight: 400;
    }

    /* ── Glass card containers ──────────────────────────────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }

    /* ── Section headers ────────────────────────────────────────────── */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e0e0e0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Result display card ────────────────────────────────────────── */
    .result-box {
        background: linear-gradient(135deg, rgba(0, 210, 255, 0.08), rgba(123, 47, 247, 0.08));
        border: 1px solid rgba(0, 210, 255, 0.2);
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 1rem;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #f0f0f0;
    }
    .result-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #00d2ff;
        margin-bottom: 0.4rem;
    }

    /* ── Detected language tag ──────────────────────────────────────── */
    .lang-tag {
        display: inline-block;
        background: linear-gradient(135deg, #7b2ff7, #ff6ac1);
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* ── Stat cards in sidebar ──────────────────────────────────────── */
    .stat-card {
        background: linear-gradient(135deg, rgba(123, 47, 247, 0.15), rgba(0, 210, 255, 0.15));
        border: 1px solid rgba(123, 47, 247, 0.25);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d2ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.55);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.2rem;
    }

    /* ── Button styling ─────────────────────────────────────────────── */
    .stButton > button {
        border-radius: 12px;
        height: 52px;
        font-size: 15px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 24px rgba(123, 47, 247, 0.3);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7b2ff7, #00d2ff) !important;
    }

    /* ── History table ──────────────────────────────────────────────── */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Footer ─────────────────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.35);
        font-size: 0.85rem;
        padding: 2rem 0 1rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 3rem;
    }
    .footer a {
        color: #7b2ff7;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
if "history_manager" not in st.session_state:
    st.session_state.history_manager = HistoryManager()

if "translation_result" not in st.session_state:
    st.session_state.translation_result = None

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""


# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🌍 Real-Time AI Language Translator</h1>
    <p>Translate text and voice across 107 languages instantly — powered by AI</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Settings & Stats
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # Auto-detect toggle
    auto_detect = st.toggle("🔍 Auto-detect source language", value=True)

    st.markdown("---")

    # Live stats
    st.markdown("## 📊 Dashboard Stats")

    entry_count = st.session_state.history_manager.get_entry_count()

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{TOTAL_LANGUAGES}</div>
        <div class="stat-label">Languages Supported</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{entry_count}</div>
        <div class="stat-label">Translations Made</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # About section
    st.markdown("## ℹ️ About")
    st.caption(
        "A modular AI-powered language translator with real-time voice I/O, "
        "built with Python, Streamlit, deep-translator, SpeechRecognition, and gTTS."
    )
    st.caption("Perfect for college AI project presentations.")


# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE SELECTION — Source & Target
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🌐 Choose Languages</div>', unsafe_allow_html=True)

lang_col1, lang_col2 = st.columns(2)

with lang_col1:
    # Source language dropdown (disabled if auto-detect is on)
    if auto_detect:
        st.selectbox(
            "📤 Source Language",
            options=["Auto-Detect (Recommended)"],
            disabled=True,
            key="src_display",
        )
        source_code = "auto"
    else:
        source_name = st.selectbox(
            "📤 Source Language",
            options=LANGUAGE_NAMES,
            index=LANGUAGE_NAMES.index("English"),
            key="src_lang",
        )
        source_code = LANGUAGES[source_name]

with lang_col2:
    # Target language dropdown
    target_name = st.selectbox(
        "📥 Target Language",
        options=LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index("Hindi"),
        key="dest_lang",
    )
    target_code = LANGUAGES[target_name]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT — Text Input & Voice Input (Two Columns)
# ─────────────────────────────────────────────────────────────────────────────
col_text, col_voice = st.columns([1, 1], gap="large")

# ── LEFT COLUMN: Text Translation ──────────────────────────────────────────
with col_text:
    st.markdown('<div class="section-header">📝 Text Translation</div>', unsafe_allow_html=True)

    text_input = st.text_area(
        "Enter text to translate:",
        height=160,
        placeholder="Type or paste any text here… No character limit!",
        key="text_input_area",
    )

    if st.button("✨ Translate Text", type="primary", use_container_width=True, key="btn_translate"):
        if text_input.strip():
            with st.spinner("🔄 Translating..."):
                result = translator_handler.translate_text(
                    text_input.strip(), source_code, target_code
                )
                st.session_state.translation_result = result

                # Save to history
                st.session_state.history_manager.add_entry(
                    original_text=text_input.strip(),
                    src_language=result["src_language_name"],
                    translated_text=result["translated_text"],
                    dest_language=result["dest_language_name"],
                    input_method="text",
                )
        else:
            st.warning("⚠️ Please enter some text to translate.")


# ── RIGHT COLUMN: Voice Translation ───────────────────────────────────────
with col_voice:
    st.markdown('<div class="section-header">🎤 Voice Translation</div>', unsafe_allow_html=True)

    st.info("Click the button below, then speak into your microphone. "
            "Your speech will be recognized, translated, and converted to audio.")

    if st.button("🎙️ Start Voice Translation", type="secondary", use_container_width=True, key="btn_voice"):
        # Determine the recognition language code
        # SpeechRecognition uses locale codes like 'en-US', 'hi-IN'
        recognition_lang = source_code if source_code != "auto" else "en-US"

        with st.spinner("🎤 Listening... Speak now!"):
            stt_result = voice_handler.speech_to_text(lang=recognition_lang)

        if stt_result["success"]:
            st.session_state.voice_text = stt_result["text"]
            st.success(f"✅ **Recognized:** {stt_result['text']}")

            # Translate the recognized speech
            with st.spinner("🔄 Translating..."):
                result = translator_handler.translate_text(
                    stt_result["text"], source_code, target_code
                )
                st.session_state.translation_result = result

                # Save to history
                st.session_state.history_manager.add_entry(
                    original_text=stt_result["text"],
                    src_language=result["src_language_name"],
                    translated_text=result["translated_text"],
                    dest_language=result["dest_language_name"],
                    input_method="voice",
                )
        else:
            st.error(f"❌ {stt_result['error']}")


# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATION RESULT DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.translation_result:
    result = st.session_state.translation_result

    st.markdown("---")
    st.markdown('<div class="section-header">📄 Translation Result</div>', unsafe_allow_html=True)

    # Show detected language tag
    if result.get("src_language_name"):
        st.markdown(
            f'<span class="lang-tag">🔍 Detected: {result["src_language_name"]}</span>'
            f'&nbsp;&nbsp;→&nbsp;&nbsp;'
            f'<span class="lang-tag">🎯 Target: {result["dest_language_name"]}</span>',
            unsafe_allow_html=True,
        )

    # Show error if any
    if result.get("error"):
        st.warning(f"⚠️ Translation returned with a warning: {result['error']}")

    # Translated text in a styled box
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Translated Text</div>
        {result["translated_text"]}
    </div>
    """, unsafe_allow_html=True)

    # ── Audio Playback ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">🔊 Listen to Translation</div>', unsafe_allow_html=True)

    tts_result = voice_handler.text_to_speech(
        result["translated_text"], target_code
    )

    if tts_result["success"] and tts_result["audio_path"]:
        st.audio(tts_result["audio_path"], format="audio/mp3")
    elif tts_result.get("error"):
        st.warning(f"⚠️ Audio generation issue: {tts_result['error']}")


# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATION HISTORY PANEL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">📜 Translation History</div>', unsafe_allow_html=True)

with st.expander("View Translation History", expanded=False):
    history_df = st.session_state.history_manager.get_history()

    if not history_df.empty:
        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": st.column_config.TextColumn("🕐 Time", width="medium"),
                "original_text": st.column_config.TextColumn("📝 Original", width="large"),
                "src_language": st.column_config.TextColumn("📤 From", width="small"),
                "translated_text": st.column_config.TextColumn("🌐 Translated", width="large"),
                "dest_language": st.column_config.TextColumn("📥 To", width="small"),
                "input_method": st.column_config.TextColumn("🔧 Method", width="small"),
            },
        )

        # Action buttons
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])

        with btn_col1:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.history_manager.clear_history()
                st.rerun()

        with btn_col2:
            csv_data = st.session_state.history_manager.export_csv()
            st.download_button(
                "📥 Export CSV",
                data=csv_data,
                file_name="translation_history.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.info("📭 No translations yet. Start translating to build your history!")


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🚀 Real-Time AI Language Translator Device &nbsp;|&nbsp;
    107 Languages &nbsp;|&nbsp;
    Voice I/O &nbsp;|&nbsp;
    Built with Python + Streamlit<br>
    Designed for College AI Project Presentation
</div>
""", unsafe_allow_html=True)

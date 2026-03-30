"""
translator.py — Translation Engine for Real-Time AI Language Translator
=======================================================================
Uses deep-translator (GoogleTranslator) for reliable, rate-limit-free translations.
Supports auto-detection, 100+ languages, and unlimited text via chunking.
"""

import logging
from deep_translator import GoogleTranslator
from config import LANGUAGES, CODE_TO_LANG, MAX_CHUNK_SIZE

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("translator")


class TranslatorHandler:
    """
    Handles all translation operations.
    
    Uses GoogleTranslator from deep-translator which is:
    - Free and unlimited (no API key needed)
    - Stable (unlike googletrans which crashes frequently)
    - Supports 100+ languages with auto-detection
    """

    def translate_text(self, text, src_lang="auto", dest_lang="en"):
        """
        Translate text from source to destination language.
        
        For long texts, automatically splits into chunks to bypass
        the 5000-character API limit, then joins the results.

        Args:
            text (str):      The text to translate.
            src_lang (str):  Source language code, or 'auto' for detection.
            dest_lang (str): Target language code (e.g., 'hi', 'fr', 'es').

        Returns:
            dict: {
                'translated_text': str,   — the translated output
                'src_detected': str,      — detected source language code
                'dest': str,              — target language code
                'src_language_name': str, — human-readable source language
                'dest_language_name': str — human-readable target language
            }
        """
        # Guard: empty input
        if not text or not text.strip():
            return {
                "translated_text": "",
                "src_detected": src_lang,
                "dest": dest_lang,
                "src_language_name": "",
                "dest_language_name": CODE_TO_LANG.get(dest_lang, dest_lang),
            }

        try:
            # ── Step 1: Create the translator instance ──────────────────
            translator = GoogleTranslator(source=src_lang, target=dest_lang)

            # ── Step 2: Chunk long text to avoid API limits ─────────────
            chunks = self._split_text(text, MAX_CHUNK_SIZE)
            translated_chunks = []

            for chunk in chunks:
                result = translator.translate(chunk)
                translated_chunks.append(result if result else "")

            translated_text = " ".join(translated_chunks)

            # ── Step 3: Detect source language ──────────────────────────
            # deep-translator doesn't return detected lang directly,
            # so we do a small detection call if source was 'auto'
            detected_code = src_lang
            if src_lang == "auto":
                detected_code = self._detect_language(text[:500])

            # ── Step 4: Build result dictionary ─────────────────────────
            src_name = CODE_TO_LANG.get(detected_code, detected_code)
            dest_name = CODE_TO_LANG.get(dest_lang, dest_lang)

            logger.info(f"Translated {len(text)} chars: {src_name} → {dest_name}")

            return {
                "translated_text": translated_text,
                "src_detected": detected_code,
                "dest": dest_lang,
                "src_language_name": src_name,
                "dest_language_name": dest_name,
            }

        except Exception as e:
            # Log the error and return original text as fallback
            logger.error(f"Translation error: {e}")
            return {
                "translated_text": text,
                "src_detected": src_lang,
                "dest": dest_lang,
                "src_language_name": CODE_TO_LANG.get(src_lang, "Unknown"),
                "dest_language_name": CODE_TO_LANG.get(dest_lang, dest_lang),
                "error": str(e),
            }

    def _detect_language(self, text):
        """
        Detect the language of the given text using Google Translate.

        Args:
            text (str): Sample text (first 500 chars is enough).

        Returns:
            str: Detected ISO language code (e.g., 'en', 'hi').
        """
        try:
            detected = GoogleTranslator(source="auto", target="en").translate(text)
            # We use a separate detection approach
            from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
            # Fallback: use the langdetect library if available
            try:
                from langdetect import detect
                return detect(text)
            except ImportError:
                return "auto"
        except Exception:
            return "auto"

    def _split_text(self, text, max_size):
        """
        Split long text into chunks for translation.
        
        Splits on sentence boundaries (periods, newlines) when possible
        to maintain translation quality.

        Args:
            text (str):     The full text to split.
            max_size (int): Maximum characters per chunk.

        Returns:
            list[str]: List of text chunks.
        """
        # Short text doesn't need splitting
        if len(text) <= max_size:
            return [text]

        chunks = []
        current_chunk = ""

        # Split by sentences (rough heuristic using '. ' and newlines)
        sentences = text.replace("\n", ". ").split(". ")

        for sentence in sentences:
            # If adding this sentence exceeds the limit, save current chunk
            if len(current_chunk) + len(sentence) + 2 > max_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += ". " + sentence if current_chunk else sentence

        # Don't forget the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def get_language_name(self, lang_code):
        """Get human-readable language name from ISO code."""
        return CODE_TO_LANG.get(lang_code, lang_code)

    def get_supported_languages(self):
        """Return sorted list of all supported language names."""
        return sorted(LANGUAGES.keys())


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL INSTANCE — import this in other modules
# ─────────────────────────────────────────────────────────────────────────────
translator_handler = TranslatorHandler()

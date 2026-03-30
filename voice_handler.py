"""
voice_handler.py — Voice I/O Module for Real-Time AI Language Translator
========================================================================
Handles Speech-to-Text (microphone → text) and Text-to-Speech (text → audio).
Uses SpeechRecognition for STT and gTTS for TTS with full error handling.
"""

import logging
import tempfile
import os
import speech_recognition as sr
from gtts import gTTS
from config import (
    VOICE_LISTEN_TIMEOUT,
    VOICE_PHRASE_TIME_LIMIT,
    VOICE_ENERGY_THRESHOLD,
)

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("voice_handler")


class VoiceHandler:
    """
    Manages all voice input/output operations.

    - Speech-to-Text: Captures audio from the microphone and converts
      it to text using Google's Web Speech API (free, no key needed).
    - Text-to-Speech: Converts translated text to an MP3 audio file
      using Google Text-to-Speech (gTTS).
    
    The microphone is initialized lazily (only when needed) to prevent
    crashes on systems without a microphone connected.
    """

    def __init__(self):
        """Initialize the speech recognizer (microphone is lazy-loaded)."""
        self.recognizer = sr.Recognizer()
        # Set energy threshold for better noise handling
        self.recognizer.energy_threshold = VOICE_ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True

    def speech_to_text(self, lang="en-US"):
        """
        Record audio from the microphone and convert to text.

        Uses Google Web Speech API for recognition. The method handles
        ambient noise calibration automatically.

        Args:
            lang (str): Language code for speech recognition
                        (e.g., 'en-US', 'hi-IN', 'fr-FR').

        Returns:
            dict: {
                'success': bool,  — whether recognition was successful
                'text': str,      — recognized text (empty on failure)
                'error': str      — error message (empty on success)
            }
        """
        try:
            # ── Step 1: Open the microphone ─────────────────────────────
            mic = sr.Microphone()

            with mic as source:
                # Calibrate for background noise (1 second)
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                # ── Step 2: Listen for speech ──────────────────────────
                logger.info(f"Listening (lang={lang}, timeout={VOICE_LISTEN_TIMEOUT}s)...")
                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_LISTEN_TIMEOUT,
                    phrase_time_limit=VOICE_PHRASE_TIME_LIMIT,
                )

            # ── Step 3: Convert speech to text via Google API ──────────
            text = self.recognizer.recognize_google(audio, language=lang)
            logger.info(f"Recognized: '{text[:80]}...'")

            return {"success": True, "text": text, "error": ""}

        # ── Error handling for all known failure modes ──────────────────
        except sr.WaitTimeoutError:
            msg = "No speech detected. Please try again and speak clearly."
            logger.warning(msg)
            return {"success": False, "text": "", "error": msg}

        except sr.UnknownValueError:
            msg = "Could not understand the audio. Please speak more clearly."
            logger.warning(msg)
            return {"success": False, "text": "", "error": msg}

        except sr.RequestError as e:
            msg = f"Speech recognition service error: {str(e)}"
            logger.error(msg)
            return {"success": False, "text": "", "error": msg}

        except OSError as e:
            msg = (
                "Microphone not found or not accessible. "
                "Please check your microphone connection and permissions."
            )
            logger.error(f"{msg} — {e}")
            return {"success": False, "text": "", "error": msg}

        except Exception as e:
            msg = f"Unexpected voice input error: {str(e)}"
            logger.error(msg)
            return {"success": False, "text": "", "error": msg}

    def text_to_speech(self, text, lang_code="en"):
        """
        Convert text to speech and save as an MP3 file.

        Uses Google Text-to-Speech (gTTS) to generate natural-sounding
        audio. The file is saved to a temporary directory.

        Args:
            text (str):      The text to convert to speech.
            lang_code (str): ISO language code (e.g., 'en', 'hi', 'fr').

        Returns:
            dict: {
                'success': bool,    — whether TTS was successful
                'audio_path': str,  — path to the MP3 file (None on failure)
                'error': str        — error message (empty on success)
            }
        """
        # Guard: empty text
        if not text or not text.strip():
            return {"success": False, "audio_path": None, "error": "No text provided"}

        try:
            # ── Step 1: Generate speech audio ──────────────────────────
            # slow=False for natural speaking speed
            tts = gTTS(text=text, lang=lang_code, slow=False)

            # ── Step 2: Save to a temporary MP3 file ───────────────────
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp3", prefix="translator_tts_"
            )
            temp_path = temp_file.name
            temp_file.close()

            tts.save(temp_path)
            logger.info(f"TTS audio saved: {temp_path} ({os.path.getsize(temp_path)} bytes)")

            return {"success": True, "audio_path": temp_path, "error": ""}

        except Exception as e:
            msg = f"Text-to-speech error: {str(e)}"
            logger.error(msg)
            return {"success": False, "audio_path": None, "error": msg}

    def cleanup_temp_files(self, file_path):
        """
        Remove a temporary audio file after playback.

        Args:
            file_path (str): Path to the file to delete.
        """
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"Could not delete temp file: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL INSTANCE — import this in other modules
# ─────────────────────────────────────────────────────────────────────────────
voice_handler = VoiceHandler()

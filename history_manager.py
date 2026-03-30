"""
history_manager.py — Translation History Manager
=================================================
Stores, retrieves, and exports translation history using pandas + CSV.
Provides persistent storage across sessions and an export feature.
"""

import logging
import os
import pandas as pd
from datetime import datetime
from config import HISTORY_FILE, HISTORY_DISPLAY_LIMIT

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("history_manager")

# Column schema for the history DataFrame
HISTORY_COLUMNS = [
    "timestamp",        # When the translation was made
    "original_text",    # Input text
    "src_language",     # Detected/selected source language name
    "translated_text",  # Output text
    "dest_language",    # Target language name
    "input_method",     # 'text' or 'voice'
]


class HistoryManager:
    """
    Manages translation history with CSV persistence.
    
    - Automatically loads history from CSV on initialization
    - Saves every new entry to disk immediately
    - Provides methods to query, clear, and export history
    """

    def __init__(self, history_file=HISTORY_FILE):
        """
        Initialize the history manager.

        Args:
            history_file (str): Path to the CSV file for persistence.
        """
        self.history_file = history_file

        # Create an empty DataFrame with the defined schema
        self.history_df = pd.DataFrame(columns=HISTORY_COLUMNS)

        # Load existing history from disk if available
        self._load_from_disk()

    def _load_from_disk(self):
        """Load history from CSV file if it exists."""
        try:
            if os.path.exists(self.history_file):
                self.history_df = pd.read_csv(self.history_file)
                logger.info(f"Loaded {len(self.history_df)} history entries from {self.history_file}")
        except Exception as e:
            logger.warning(f"Could not load history file: {e}")
            self.history_df = pd.DataFrame(columns=HISTORY_COLUMNS)

    def _save_to_disk(self):
        """Save current history DataFrame to CSV."""
        try:
            self.history_df.to_csv(self.history_file, index=False)
        except Exception as e:
            logger.error(f"Could not save history: {e}")

    def add_entry(self, original_text, src_language, translated_text,
                  dest_language, input_method="text"):
        """
        Add a new translation to the history.

        Args:
            original_text (str):   The original input text.
            src_language (str):    Source language name (e.g., 'English').
            translated_text (str): The translated output text.
            dest_language (str):   Target language name (e.g., 'Hindi').
            input_method (str):    'text' or 'voice'.
        """
        new_entry = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original_text": original_text[:200],       # Truncate for display
            "src_language": src_language,
            "translated_text": translated_text[:200],   # Truncate for display
            "dest_language": dest_language,
            "input_method": input_method,
        }])

        # Append to the in-memory DataFrame
        self.history_df = pd.concat(
            [self.history_df, new_entry], ignore_index=True
        )

        # Persist to disk immediately
        self._save_to_disk()
        logger.info(f"History entry added: {src_language} → {dest_language}")

    def get_history(self, limit=HISTORY_DISPLAY_LIMIT):
        """
        Get recent translation history entries.

        Args:
            limit (int): Maximum number of entries to return.

        Returns:
            pd.DataFrame: Most recent entries, newest first.
        """
        return (
            self.history_df
            .tail(limit)
            .sort_index(ascending=False)
            .reset_index(drop=True)
        )

    def get_entry_count(self):
        """Return total number of history entries."""
        return len(self.history_df)

    def clear_history(self):
        """Clear all history from memory and disk."""
        self.history_df = pd.DataFrame(columns=HISTORY_COLUMNS)

        # Remove the CSV file from disk
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
                logger.info("History file deleted")
        except Exception as e:
            logger.warning(f"Could not delete history file: {e}")

        logger.info("History cleared")

    def export_csv(self):
        """
        Export history as CSV bytes for download.

        Returns:
            bytes: CSV content encoded as UTF-8 bytes.
        """
        return self.history_df.to_csv(index=False).encode("utf-8")

# 🌍 Real-Time AI Language Translator Device

A complete **Real-Time AI Language Translator** built with Python and Streamlit. Features a premium dark-themed dashboard, **107 languages**, real-time voice input/output, automatic language detection, translation history with export, and professional error handling.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 Voice Input | Record speech via microphone → auto-convert to text |
| 🔊 Voice Output | Listen to translated text via audio playback |
| 🌐 107 Languages | Full list of supported languages with searchable dropdowns |
| 🔍 Auto-Detection | Automatically detects the source language |
| 📜 History | Persistent translation history with CSV export |
| ♾️ No Limits | Handles long texts via automatic chunking |
| 🛡️ Error Handling | Graceful handling of mic, API, and network errors |
| 🎨 Premium UI | Dark glassmorphism theme with gradient animations |

---

## 🏗️ Project Architecture

```
RealTime_AI_Translator/
│
├── streamlit_app.py       # 🎨 Main Streamlit dashboard (entry point)
├── config.py              # ⚙️ Languages (107), constants, settings
├── translator.py          # 🌐 Translation engine (deep-translator)
├── voice_handler.py       # 🎤 Speech-to-Text & Text-to-Speech
├── history_manager.py     # 📜 Translation history (pandas + CSV)
│
├── requirements.txt       # 📦 Python dependencies
├── README.md              # 📄 This file
└── translation_history.csv  # 📊 Auto-generated history file
```

### Data Flow

```
┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│  Microphone   │────▶│ SpeechRecogn.  │────▶│              │
└──────────────┘     └────────────────┘     │              │
                                             │  Translator  │──▶ Translated Text
┌──────────────┐                             │  (deep-      │
│  Text Input   │───────────────────────────▶│   translator)│──▶ Audio (gTTS)
└──────────────┘                             │              │
                                             └──────┬───────┘
                                                    │
                                             ┌──────▼───────┐
                                             │   History     │
                                             │   Manager     │──▶ CSV Export
                                             └──────────────┘
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.9+** installed
- A working **microphone** (for voice features)
- **Internet connection** (for translation & speech APIs)

### 2. Install Dependencies

```bash
cd "c:\Users\aakas\Saved Games\RealTime_AI_Translator"
pip install -r requirements.txt
```

> **Windows PyAudio fix** (if you get a PyAudio installation error):
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```
> Or download the `.whl` file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### 3. Run the App

```bash
python -m streamlit run streamlit_app.py
```

The dashboard opens at **http://localhost:8501** 🎉

---

## 📋 How to Use

1. **Select Languages** — Choose source & target from the dropdowns (or use auto-detect)
2. **Text Translation** — Type/paste text → click "✨ Translate Text"
3. **Voice Translation** — Click "🎙️ Start Voice Translation" → speak into mic
4. **Listen** — Audio playback appears automatically after translation
5. **History** — Expand the history panel to view/export/clear past translations

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit (responsive dashboard) |
| Translation | deep-translator (Google Translate) |
| Speech-to-Text | SpeechRecognition + Google Web Speech API |
| Text-to-Speech | gTTS (Google Text-to-Speech) |
| Data Storage | pandas + CSV |
| Language Detection | langdetect |

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| `PyAudio` install fails | Use `pipwin install pyaudio` on Windows |
| Microphone not detected | Check system permissions & default device |
| Translation returns original text | Check internet connection |
| "No speech detected" | Speak louder / closer to mic, check timeout |
| Slow translation | Normal for free API; chunk large texts |

---

## 🎓 College Presentation Tips

- **Live Demo**: Show voice-to-voice translation (English → Hindi)
- **Architecture**: Explain the modular 5-file structure
- **Features**: Highlight 107 languages, history export, error handling
- **Code Quality**: Point out comments, type hints, and clean separation

---

## 📄 License

MIT License — Free for educational and commercial use.

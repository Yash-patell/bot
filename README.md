#  Voice Interview Bot – Home.LLC Assignment

This is an AI-powered voice interview assistant that listens to your spoken questions, transcribes them, and responds like **Yash Patel**, a candidate applying for a remote AI role at **Home.LLC**. The bot uses:

-  **Gemini API** (Generative AI from Google)
-  **Google Cloud Text-to-Speech**
-  Streamlit frontend for interactive experience

---

## 🚀 Features

✅ Speak interview questions using your microphone  
✅ Bot responds like Yash Patel with realistic answers  
✅ Hear the response using natural Indian English voice (Google TTS)  
✅ Context-aware: remembers personality and resume background  
✅ Works locally or can be deployed on [Streamlit Cloud](https://streamlit.io/cloud)

---

<br>

## 🛠️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/voice-interview-bot.git
cd voice-interview-bot
```

### 2. Install requirement.txt
```bash
pip install requirements.txt
```

### 3. Enter your credentials Gemini api key,google cloud Speech to text api key
. Put you key inside the .streamlit/secrets.toml 

### 4. Run the main app
```bash
streamlit run bot_main.py
```

<br>

## File Structure

```bash
voice-interview-bot/
│
├── bot_main.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .gitignore # Git ignored files
│
├── .streamlit/
│ └── secrets.toml # API keys (used only in deployment)
│
└── README.md # This file
```

<br>

### Demo Videos (google drive link for demo videos) - https://drive.google.com/drive/folders/1nB7cH1yPRCLEaFu5gWuT2Ehfk83P1ZtD?usp=sharing


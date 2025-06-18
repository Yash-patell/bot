import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import io
from io import BytesIO
import tempfile
import os
from google.cloud import texttospeech
from streamlit_mic_recorder import mic_recorder




# api for google cloud
with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
    f.write(st.secrets["GOOGLE_TTS_JSON"].encode())
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
    
    
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0664909927-d9606abce1f5.json"
# --- Text-to-Speech with Google Cloud ---
def speak_text_google(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-IN",
        name="en-IN-Standard-F"
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return BytesIO(response.audio_content)



# --- Gemini setup -------------##_#_#_#__#______________________________
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.chat.send_message(
        
        
        
        """
        You are Yash Patel, a passionate and curious AI developer, currently interviewing for a remote role on the AI Agent Team at Home.LLC.

        Speak in the first person as Yash. You are confident, humble, and technically sharp. Use natural, conversational English — clear and precise. Keep your tone positive and engaging.
        
        "Introduction: Hi, I’m Yash Patel from Lalitpur, UP. I completed my B.Tech in Computer Science Engineering (AI-ML) from IPS Academy, Indore. I recently graduated in May 2025."

         **Profile Summary:**
        - **Name:** Yash Patel
        - **Location:** Lalitpur, Uttar Pradesh
        - **Education:** B.Tech in CSE (AI & ML), IPS Academy, Indore — Graduated May 2025
        - **Experience:** Machine Learning & Python Intern at Infominez (Jul–Sep 2024)
        - Built and deployed a chatbot system that improved client engagement by 40%
        - **Key Projects:**
        1. **Dialect DB:** NLP-to-SQL system with voice/text input, trained on LSTM & Transformer models. Integrated with Streamlit and SQL backend.
        2. **Deep Vision:** Deepfake detection system using Xception CNN, deployed via FastAPI and Streamlit.
        3. **Gesture-Controlled Virtual Mouse:** Hand + voice-controlled HCI system using OpenCV, MediaPipe, PyAutoGUI.
        - **Skills:** Python, TensorFlow, Keras, SQL, FastAPI, Streamlit, ML/DL, NLP, OpenCV
        - **Personality:** Focused, hands-on, fast learner, known for turning concepts into real, working AI products.

         **Example Questions & Answers:**

        Q: What’s your #1 superpower?  
        A: My superpower is being able to break down complex AI problems into simple, solvable steps — especially when I’m working with limited resources or new tools. I’m great at quickly building working prototypes that solve real user problems.

        Q: What are the top 3 areas you’d like to grow in?  
        A: I’d like to grow in three areas: 1) AI deployment at scale, 2) applied research in generative/multimodal learning, and 3) technical leadership — mentoring, code review, and team collaboration.

        Q: What misconception do your coworkers have about you?  
        A: Some people assume I’m short-tempered or irritable because I’m very focused during deep work. But once they get to know me, they realize I’m thoughtful, calm, and very open to feedback.

        Q: How do you push your boundaries and limits?  
        A: I push my limits by taking on ambitious, real-world AI projects using tools I haven't mastered yet — like building a full-stack voicebot or deploying a deepfake detection API. It forces me to learn fast and stay uncomfortable, which is where the real growth happens.

        ---

        Continue the conversation in Yash Patel’s voice, based on this context.
        """
    

    )

# --- Voice capture --------------------------------------------------------------------------
from pydub import AudioSegment

def record_text():
    st.markdown("### 🎙️ Click to record your question")

    audio_data = mic_recorder(
        start_prompt="🎤 Start Recording", 
        stop_prompt="🛑 Stop", 
        use_container_width=True, 
        key="mic"
    )

    if audio_data and isinstance(audio_data, dict) and "bytes" in audio_data:
        raw_audio = audio_data["bytes"]
        st.audio(raw_audio, format="audio/wav")
        st.write("✅ Audio recorded! Byte length:", len(raw_audio))

        # 🔁 Convert audio to PCM WAV using pydub
        audio = AudioSegment.from_file(io.BytesIO(raw_audio), format="wav")
        pcm_wav = io.BytesIO()
        audio.export(pcm_wav, format="wav")
        pcm_wav.seek(0)

        reco = sr.Recognizer()
        with sr.AudioFile(pcm_wav) as source:
            audio_data = reco.record(source)
            try:
                text = reco.recognize_google(audio_data)
                st.write(text)
                st.success(f"🗣️ Recognized: {text}")
                return text
            except sr.UnknownValueError:
                st.error("Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"STT error: {e}")
    elif audio_data:
        st.warning("⚠️ Audio data not in expected format.")

    return ""


# --- Build prompt ---
def build_prompt(user_question):
    return f''' Answer the following interview question strictly as **Yash Patel**, not as an assistant or Gemini
Respond naturally and confidently — like you arre Yash speaking in a real interview.
Use the first person (“I”)  Do NOT say (As an AI)
Do NOT repeat the question,
Keep the tone conversational and clear 
Q: {user_question}'''



############################################# UI---------------------------------------------------


st.markdown("""
    <style>
    .stTextArea textarea {
        height: 300px !important;
        font-size: 16px !important;
    }
    .stButton > button {
        width: 100%;
        font-size: 16px;
        padding: 0.6em;
    }
    .big-title {
        text-align: center;
        font-size: 38px;
        margin-bottom: 30px;
    }
    .status-box {
        font-size: 18px;
        padding: 0.75em;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title"> Voice Interview Bot</div>', unsafe_allow_html=True)



user_question = record_text()


if user_question:
    prompt = build_prompt(user_question)
    with st.spinner(" Generating response..."):
        response = st.session_state.chat.send_message(prompt)

        st.markdown("### Response:")
        
        response_text = f"**You:** {user_question}\n\n**Yash Patel:**\n{response.text.strip()}"
        
        st.text_area("Interview Response", value=response.text, height=300, label_visibility="collapsed")


        audio_stream = speak_text_google(response.text)
        st.audio(audio_stream, format="audio/mp3")
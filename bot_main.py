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
from google.cloud import speech
import json  # Add at the top
import json
from google.oauth2 import service_account




try:
    tts_creds_info = json.loads(st.secrets["GOOGLE_TTS_JSON"])
    tts_credentials = service_account.Credentials.from_service_account_info(tts_creds_info)
    tts_client_global = texttospeech.TextToSpeechClient(credentials=tts_credentials)
except KeyError:
    st.error("Missing GOOGLE_TTS_JSON secret. Please configure it in Streamlit Cloud.")
    st.stop() # Stop the app if secrets are missing

# ... (rest of your global Gemini setup, etc.) ...

# --- Text-to-Speech with Google Cloud ---
def speak_text_google(text):
    # USE THE GLOBALLY INITIALIZED CLIENT HERE, DO NOT RE-INITIALIZE
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-IN",
        name="en-IN-Standard-F"
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client_global.synthesize_speech( # <--- Changed this line
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





def record_text():
    st.markdown("### Click to record your question and Stop once you are done ")

    audio_data = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="🛑 Stop",
        use_container_width=True,
        key="mic"
    )

    if audio_data and isinstance(audio_data, dict) and "bytes" in audio_data:
        raw_audio = audio_data["bytes"]
        recorded_sample_rate = audio_data.get("sample_rate") # Get actual sample rate
        # st.audio(raw_audio, format="audio/webm") # Display the recorded WebM audio
        st.write(f"✅ Audio recorded! Byte length: {len(raw_audio)}")
        # if recorded_sample_rate:
        #     st.write(f"Detected sample rate from mic: {recorded_sample_rate} Hz")
        # else:
        #     st.warning("Could not detect sample rate from mic_recorder. Defaulting to 48000 Hz.")


        try:
            stt_creds_info = json.loads(st.secrets["GOOGLE_STT_JSON"])
            stt_credentials = service_account.Credentials.from_service_account_info(stt_creds_info)
            stt_client = speech.SpeechClient(credentials=stt_credentials)

            audio = speech.RecognitionAudio(content=raw_audio)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=recorded_sample_rate if recorded_sample_rate else 48000, # Use detected rate, fall back to 48000
                language_code="en-US" # Essential!
            )

            response = stt_client.recognize(config=config, audio=audio)
            # st.write("📜 Raw STT Response:", response)

            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                st.success(f"🗣️ Recognized: {transcript}")
                return transcript
            else:
                st.warning("⚠️ No speech recognized. Try again.")
                st.info("Ensure microphone is working, speak clearly, and check background noise.")

        except KeyError:
            st.error("Missing GOOGLE_STT_JSON secret. Please configure it in Streamlit Cloud.")
        except Exception as e:
            st.error(f"❌ STT Error: {e}")
    else:
       return None

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
        st.audio(audio_stream, format="audio/mp3",autoplay=True,loop = False)
        st.write("This is the response audio from the bot you can Download it also")
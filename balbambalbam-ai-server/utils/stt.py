import base64
import speech_recognition as sr
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file_conversion import base64_to_wav

def create_user_text(audio_base64):
    audio_file_path = base64_to_wav(audio_base64)
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as audio_file:
        audio_data = recognizer.record(audio_file)
    return recognizer.recognize_google(audio_data, language='ko-KR')
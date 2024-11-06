import re
import json
import os
import sys
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_processing import separate_text, calculate_accuracy
from utils.stt import create_user_text
from utils.waveform import draw_waveform
from utils.audio_data import extract_dataframe_base64, process_and_save_audio_base64

async def get_feedback_request_test(request: Request) -> JSONResponse:
    print("=== request : ai/feedback_test ===")

    # get request data
    data = await request.json()
    if data is None:
        print("Missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")

    # get parameters
    try:
        user_audio = data.get("userAudio")
        correct_audio = data.get("correctAudio")
        correct_text = data.get("pronunciation")
        print("request text : ", correct_text)
    except KeyError as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")

    # Initialize default values
    user_text = ''
    user_mistaken_index = []
    user_accuracy = 0
    user_recommend_phoneme = []
    user_recommend_last_phoneme = []

    # Extract user text and validate (in case of word / sentence)
    if len(correct_text) > 1:
        try:
            user_text = create_user_text(user_audio)
            
            # Trim whitespace if text is a word
            if len(correct_text) < 5:
                user_text = re.sub(r"\s+", "", user_text)
            
            # Validate user text length
            if len(user_text) >= len(correct_text) * 2:
                raise ValueError("User text is too long")
            elif len(user_text) * 2 < len(correct_text):
                raise ValueError("User text is too short")

            print("user text : ", user_text)
        except ValueError as ve:
            print(ve)
            raise HTTPException(status_code=422, detail=f"{ve}, please request re-recording")
        except Exception as e:
            print("failed to extract user text (STT)", e)
            raise HTTPException(status_code=422, detail="failed to extract user text (STT), please request re-recording")

        # Separate text
        try:
            separated_user_text = await separate_text(user_text) if user_text else None
            separated_correct_text = await separate_text(correct_text)
        except Exception as e:
            print("failed to separate text", e)
            raise HTTPException(status_code=500, detail="failed to separate text")

        # Calculate accuracy, extract mistaken index & phoneme
        try:
            user_accuracy, user_mistaken_index, user_recommend_phoneme, user_recommend_last_phoneme = await calculate_accuracy(separated_correct_text, separated_user_text)
            print("Accuracy:", user_accuracy)
            print("Mistaken indices:", user_mistaken_index)
            print("Mistaken phonemes:", user_recommend_phoneme)
            print("Mistaken last phonemes:", user_recommend_last_phoneme)
        except Exception as e:
            print("failed to calculate accuracy", e)
            raise HTTPException(status_code=500, detail="failed to calculate accuracy")

    # Extract duration & draw waveform
    try:
        user_audio_duration, user_audio_waveform = draw_waveform(user_audio, '#644829') if user_audio else (None, None)
        correct_audio_duration, correct_audio_waveform = draw_waveform(correct_audio, '#ED7161') if correct_audio else (None, None)
        print("User audio duration:", user_audio_duration)
        print("Correct audio duration:", correct_audio_duration)
    except Exception as e:
        print("failed to extract duration & draw waveform", e)
        raise HTTPException(status_code=500, detail="failed to extract duration & draw waveform")
    
    # Extravt Audio Dataframe
    try :
        processed_ai_audio = process_and_save_audio_base64(correct_audio)
        processed_user_audio = process_and_save_audio_base64(user_audio)
        ai_df, user_df = extract_dataframe_base64(processed_ai_audio, processed_user_audio)
    except Exception as e:
        print("failed to extract audio dataframe", e)
        raise HTTPException(status_code=500, detail="failed to extract audio")

    # Make output data
    output_data = {
        "userText": user_text,
        "userMistakenIndexes": user_mistaken_index,
        "userAccuracy": user_accuracy,
        "recommendedPronunciations": user_recommend_phoneme,
        "recommendedLastPronunciations": user_recommend_last_phoneme,
        "userAudio" : processed_user_audio,
        "userAmplitude" : user_df,
        "correctAudio" : processed_ai_audio,
        "correctAmplitude" : ai_df,
        }
    
    print("=== fin : ai/feedback_test ===")
    return JSONResponse(content=output_data, status_code=200)

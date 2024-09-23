import re
import json
import os
import sys
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_processing import separate_text, find_phoneme_errors
from utils.stt import create_user_text

async def get_test_request(request: Request) -> JSONResponse:
    print("=== request : ai/test ===")
    
    # get request data
    data = await request.json()
    if data is None:
        print("Missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")

    # get parameters
    try:
        user_audio = data.get("userAudio")
        correct_text = data.get("correctText")
        print("request text : ", correct_text)
    except KeyError as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
        
    # extract user text
    try:
        user_text = create_user_text(user_audio)
        print("user text : ", user_text)
        
        if len(user_text) >= len(correct_text)*2:
            raise ValueError("User text is too long")
    
        if len(user_text)*2 < len(correct_text):
            raise ValueError("User text is too short")
    
    except ValueError as ve:
        print(ve)
        raise HTTPException(status_code=422, detail=f"{ve}, please request re-recording")
    except Exception as e:
        print("failed to extract user text (STT)", e)
        raise HTTPException(status_code=422, detail="failed to extract user text (STT), please request re-recording")

    # separation text
    try:
        separated_user_text = await separate_text(user_text)
        separated_correct_text = await separate_text(correct_text)
    except Exception as e:
        print("failed to separate text", e)
        raise HTTPException(status_code=500, detail="failed to separate text")

    # find weak phoneme
    try:
        user_weak_phoneme, user_weak_phoneme_last = await find_phoneme_errors(separated_user_text, separated_correct_text)
        print("user weak phoneme : ", user_weak_phoneme)
        print("user weak phoneme last : ", user_weak_phoneme_last)
    except Exception as e:
        print("failed to find weak phoneme", e)
        raise HTTPException(status_code=500, detail="failed to find weak phoneme")

    # make output data
    output_data = {
        "userWeakPhoneme": user_weak_phoneme,
        "userWeakPhonemeLast": user_weak_phoneme_last,
        "userText": user_text,
    }
    
    print("=== fin : ai/test ===")
    return JSONResponse(content=output_data, status_code=200)

import json
import os
import sys
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.tts import generate_voice

async def get_voice_request(request: Request) -> JSONResponse:
    print("=== request : ai/voice ===")

    # get request data
    data = await request.json()
    if data is None:
        print("Missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")

    # get parameters
    try:
        gender = data.get("gender")
        age = data.get("age")
        text = data.get("text")
        print("age : ", age)
        print("gender : ", gender)
        print("request text : ", text)
    except KeyError as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    # generate voice
    try:
        correct_audio = await generate_voice(gender, age, text)
    except Exception as e:
        print("failed to generate voice (TTS)")
        raise HTTPException(status_code=500, detail="failed to generate voice (TTS)")
    
    # make output data
    output_data = {
        "correctAudio": correct_audio,
    }
    print("=== fin : ai/voice ===")
    return JSONResponse(content=output_data, status_code=200)

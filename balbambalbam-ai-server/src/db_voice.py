from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.tts import generate_voice

async def db_get_voice_request(request: Request) -> JSONResponse:
    print("=== request : ai/db_voice ===")

    # get request data
    data = await request.json()
    if data is None:
        print("Missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")

    # get parameters
    try:
        text = data.get("text")
        print("request text : ", text)
    except KeyError as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    # generate voice
    try : 
        child_0 = await generate_voice(0, 0, text)
        adult_0 = await generate_voice(0, 20, text)
        elderly_0 = await generate_voice(0, 60, text)
        child_1 = await generate_voice(1, 0, text)
        adult_1 = await generate_voice(1, 20, text)
        elderly_1 = await generate_voice(1, 60, text)
    except Exception as e:
        print("failed to generate voice (TTS)")
        return "failed to generate voice (TTS)", 500
    
    # make output data
    output_data = {
        'child_0' : child_0,
        'adult_0' : adult_0,
        'elderly_0' : elderly_0,
        'child_1' : child_1,
        'adult_1' : adult_1,
        'elderly_1' : elderly_1
    }

    print("=== fin : ai/db_voice ===")
    return JSONResponse(content=output_data, status_code=200)

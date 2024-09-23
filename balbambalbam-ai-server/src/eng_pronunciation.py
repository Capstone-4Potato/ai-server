from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_processing import generate_eng_pronunciation

async def get_eng_pronunciation_request(request: Request) -> JSONResponse:
    print("=== request : ai/eng-pronunciation ===")
    
    data = await request.json()
    if data is None:
        print("Missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")
        
    try:
        text = data.get("text")
        print("request text : ", text)
    except Exception as e:
        print("Invalid parameters")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    try:
        eng_pronunciation = await generate_eng_pronunciation(text)
        print("eng-pronunciation : ", eng_pronunciation)
    except Exception as e:
        print("failed to generate pronunciation")
        raise HTTPException(status_code=500, detail="failed to generate pronunciation")
    
    output_data = {
        "engPronunciation": eng_pronunciation,
    }
    
    print("=== fin : ai/eng-pronunciation ===")
    return JSONResponse(content=output_data, status_code=200)

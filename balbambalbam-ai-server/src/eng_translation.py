from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
import sys
from googletrans import Translator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_processing import translate_korean_to_english

async def get_eng_translation_request(request: Request) -> JSONResponse:
    print("=== request : ai/eng-translation ===")
    
    data = await request.json()
    if data is None:
        print("Missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")
        
    try:
        text = data.get("text")
        print("request text: ", text)
    except Exception as e:
        print("Invalid parameters")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    # try:
    #     eng_translation = await translate_korean_to_english(text)
    #     print("eng-translation: ", eng_translation)
    # except Exception as e:
    #     print("failed to generate translation")
    #     raise HTTPException(status_code=500, detail="failed to generate translation")

    
    eng_translation = translate_korean_to_english(text)
    print("eng-translation: ", eng_translation)
    
    output_data = {
        "engTranslation": eng_translation,
    }
    
    print("=== fin : ai/eng-translation ===")
    return JSONResponse(content=output_data, status_code=200)

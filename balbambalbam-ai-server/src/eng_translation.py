from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
import sys
from googletrans import Translator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_processing import translate_english_to_korean

async def get_kor_translation_request(request: Request) -> JSONResponse:
    print("=== request : ai/kor-translation ===")
    
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
    
    kor_translation = translate_english_to_korean(text)
    print("kor-translation: ", kor_translation)
    
    output_data = {
        "korTranslation": kor_translation,
    }
    
    print("=== fin : ai/kor-translation ===")
    return JSONResponse(content=output_data, status_code=200)
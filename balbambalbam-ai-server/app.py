from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src import (
    get_feedback_request,
    get_feedback_request_test,
    get_test_request,
    get_voice_request,
    get_eng_pronunciation_request,
    get_eng_translation_request,
    get_kor_translation_request,
    db_get_voice_request
)

app = FastAPI()

@app.post("/ai/feedback")
async def feedback_route(request: Request):
    try:
        return await get_feedback_request(request)
    except HTTPException as e:
        raise e
    
@app.post("/ai/feedback-test")
async def feedback_route_test(request: Request):
    try:
        return await get_feedback_request_test(request)
    except HTTPException as e:
        raise e

@app.post("/ai/test")
async def test_route(request: Request):
    try:
        return await get_test_request(request)
    except HTTPException as e:
        raise e

@app.post("/ai/voice")
async def voice_route(request: Request):
    try:
        return await get_voice_request(request)
    except HTTPException as e:
        raise e

@app.post("/ai/db-voice")
async def db_voice_route(request: Request):
    try:
        return await db_get_voice_request(request)
    except HTTPException as e:
        raise e

@app.post("/ai/eng-pronunciation")
async def eng_pronunciation_route(request: Request):
    try:
        return await get_eng_pronunciation_request(request)
    except HTTPException as e:
        raise e

@app.post("/ai/eng-translation")
async def eng_translation_route(request: Request):
    try:
        return await get_eng_translation_request(request)
    except HTTPException as e:
        raise e
    
@app.post("/ai/kor-translation")
async def kor_translation_route(request: Request):
    try:
        return await get_kor_translation_request(request)
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)

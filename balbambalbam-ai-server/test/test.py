import base64
import httpx
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client_id = os.getenv('NAVER_TTS_API_ID')
client_secret = os.getenv('NAVER_TTS_API_SECRET')

if not client_id or not client_secret:
    print("Error: Environment variables for NAVER_TTS_API_ID and NAVER_TTS_API_SECRET must be set.")
    sys.exit(1)

print("client_id: ", client_id)
print("client_secret: ", client_secret)

gender = 1
age = 14
text = '아'

# Determine the speaker based on gender and age
if gender == 1:
    if age <= 14:
        speaker = 'vdain'       # Female child
    elif age <= 40:
        speaker = 'nkyunglee'   # Female young adult
    else:
        speaker = 'nsunkyung'   # Female middle-aged or older
elif gender == 0:
    if age <= 14:
        speaker = 'nhajun'      # Male child
    elif age <= 40:
        speaker = 'vdaeseong'   # Male young adult
    else:
        speaker = 'nyoungil'    # Male middle-aged or older
else:
    speaker = 'nkyunglee'       # Default speaker

# Prepare the request data
request_data = {
    "speaker": speaker,
    "volume": 5,
    "speed": 2,
    "pitch": 0,
    "format": "wav",
    "text": text
}

# Prepare the request headers
request_headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret
}

# Initialize the HTTP client and make the request
with httpx.Client() as client:
    response = client.post(
        "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts", 
        data=request_data, 
        headers=request_headers
    )

# Check the response status
if response.status_code == 200:
    print("Successfully generated voice.")
else:
    print(f"Error Code: {response.status_code}, Response: {response.text}")

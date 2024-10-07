import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client_id = os.getenv('NAVER_TTS_API_ID')
client_secret = os.getenv('NAVER_TTS_API_SECRET')

print("client_id : ", client_id)
print("client_secret : ", client_secret)
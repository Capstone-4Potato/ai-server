# 🌰 음성 및 발음 평가 API 🌰
> 본 ai-server의 코드는 음성 및 발음 평가를 위한 다양한 기능을 제공하는 Fast-API 기반의 서버이다. 주요 기능으로는 음성 생성, 음성 인식, 발음 평가, 취약음소 탐지 등이 존재한다. 상세 내용은 아래와 같다.

<br/><br/>

## ⚙️ 주요 기능 ⚙️

#### 🔸 음성 생성 (Text to Speech)
> generate_voice(text)
> 
> 텍스트를 받아 해당 텍스트의 음성 생성 후 base64 인코딩
  
  
#### 🔸 음성 인식 (Speech to Text)
> create_user_text(user_audio)

> base64로 인코딩된 음성을 받아 텍스트로 변환
  
  
#### 🔸 한국어 텍스트 분리
> seperation_text(text)
>
> 입력된 한글 텍스트를 초성, 중성, 종성으로 분리하여 배열로 반환
  
  
#### 🔸 취약음소 탐지
> find_weak_phoneme(user_text, correct_text)
>
> 사용자가 발음한 텍스트와 올바른 텍스트를 비교하여 약한 음소를 탐지하고, 이를 배열로 반환
  
  
#### 🔸 정확도 계산
> calculate_accuracy(correct_text, user_text)
>
> 사용자가 발음한 텍스트와 올바른 텍스트를 비교하여 정확도를 계산하고, 사용자가 잘못 발음한 인덱스와 추천 음소 반환
  
  
#### 🔸 파형 생성
> draw_waveform(user_audio, g_color)
> 
> base64로 인코딩된 음성 데이터를 받아 파형 이미지를 생성하고, 이를 base64로 인코딩된 문자열로 반환
  
  
#### 🔸 한국어 발음 생성
> generate_kor_pronunciation(text)
> 
> 입력된 한국어 텍스트의 발음을 생성하여 반환
  
  
#### 🔸 영어 발음 생성
> generate_eng_pronunciation(text)
> 
> 입력된 한국어 텍스트를 영어로 변환하여 반환

<br/><br/>
  
## 🛰️ HTTP Request Handler 🛰️
#### 🔸 음성 피드백 요청 (POST /ai/feedback)
> 사용자의 음성과 올바른 음성을 받아 텍스트로 변환하고, 정확도와 파형 이미지 등의 분석 결과(피드백)반환
  
  
#### 🔸 음성 생성 요청 (POST /ai/voice)
> 입력된 텍스트를 음성으로 변환하여 반환
    
  
#### 🔸 테스트 요청 (POST /ai/test)
> 사용자의 음성을 받아 텍스트로 변환하고, 발견된 취약음소 반환
  
  
#### 🔸 한국어 발음 요청 (POST /ai/kor-pronunciation)
> 입력된 한국어 텍스트의 표준 발음 반환
  
  
#### 🔸 영어 발음 요청 (POST /ai/eng-pronunciation)
> 입력된 한국어 텍스트의 로마자 표기 반환

<br/><br/>

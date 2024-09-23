import re  
import json  
import asyncio
from mtranslate import translate
from googletrans import Translator
from korean_romanizer.romanizer import Romanizer

async def separate_text(text):
    CHOSUNG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    
    separated_text = []

    for char in text:
        if char == ' ':
            # Use ['*', '*', '*'] to represent a space
            separated_text.append(['*', '*', '*'])
        elif '가' <= char <= '힣':
            # Calculate the indices for Chosung, Jungsung, and Jongsung
            char_code = ord(char) - 44032
            cho_idx = char_code // 588
            jung_idx = (char_code - (cho_idx * 588)) // 28
            jong_idx = char_code % 28
            separated_text.append([CHOSUNG[cho_idx], JUNGSUNG[jung_idx], JONGSUNG[jong_idx]])
        else:
            continue

    return separated_text


async def find_phoneme_errors(user_text, correct_text):
    phoneme_errors = {}
    last_phoneme_errors = {}

    JONGSUNG_MAPPINGS = {
        'ㄱ': 'ㄱ', 'ㄲ': 'ㄱ', 'ㄳ': 'ㄱ', 'ㄴ': 'ㄴ', 'ㄵ': 'ㄴ', 'ㄶ': 'ㄴ',
        'ㄷ': 'ㄷ', 'ㄹ': 'ㄹ', 'ㄺ': 'ㄹ', 'ㄻ': 'ㄹ', 'ㄼ': 'ㄹ', 'ㄽ': 'ㄹ', 'ㄾ': 'ㄹ', 'ㄿ': 'ㄹ', 'ㅀ': 'ㄹ',
        'ㅁ': 'ㅁ', 'ㅂ': 'ㅂ', 'ㅄ': 'ㅂ',
        'ㅅ': 'ㅅ', 'ㅆ': 'ㅅ',
        'ㅇ': 'ㅇ',
        'ㅈ': 'ㄷ', 'ㅊ': 'ㄷ', 'ㅋ': 'ㄱ', 'ㅌ': 'ㄷ', 'ㅍ': 'ㅂ', 'ㅎ': 'ㄷ'
    }

    SIMILAR_JUNGSUNG_MAP = {
        'ㅐ': ['ㅔ'], 'ㅔ': ['ㅐ'],
        'ㅙ': ['ㅞ', 'ㅚ'], 'ㅞ': ['ㅙ', 'ㅚ'], 'ㅚ': ['ㅞ', 'ㅙ'],
        'ㅒ': ['ㅖ'], 'ㅖ': ['ㅒ']
    }

    for i, correct_char in enumerate(correct_text):
        # Get the corresponding user's character, or ['*', '*', '*'] if missing
        user_char = user_text[i] if i < len(user_text) else ['*', '*', '*']

        for j, (ph_correct, ph_user) in enumerate(zip(correct_char, user_char)):
            if ph_correct == ph_user:
                continue
            elif j == 1 and ph_user in SIMILAR_JUNGSUNG_MAP.get(ph_correct, []):
                # Allow similar Jungsung phonemes to be considered correct
                continue
            else:
                if ph_correct != '*':
                    if j != 2:  # Final consonant (Jongsung)
                        phoneme_errors[ph_correct] = phoneme_errors.get(ph_correct, 0) + 1
                    else:
                        mapped_phoneme = JONGSUNG_MAPPINGS.get(ph_correct, ph_correct)
                        last_phoneme_errors[mapped_phoneme] = last_phoneme_errors.get(mapped_phoneme, 0) + 1

    return phoneme_errors, last_phoneme_errors


async def calculate_accuracy(correct_text, user_text):
    total_chars = 0
    matching_chars = 0
    mistaken_indices = []
    recommended_phonemes = []
    recommended_last_phonemes = []
    penalties = 0

    SIMILAR_JUNGSUNG_MAP = {
        'ㅐ': ['ㅔ'], 'ㅔ': ['ㅐ'],
        'ㅙ': ['ㅞ', 'ㅚ'], 'ㅞ': ['ㅙ', 'ㅚ'], 'ㅚ': ['ㅞ', 'ㅙ'],
        'ㅒ': ['ㅖ'], 'ㅖ': ['ㅒ']
    }

    for i, correct_char in enumerate(correct_text):
        # Get the corresponding user's character, or ['*', '*', '*'] if missing
        user_char = user_text[i] if i < len(user_text) else ['*', '*', '*']

        for j, (ph_correct, ph_user) in enumerate(zip(correct_char, user_char)):
            total_chars += 1

            if ph_correct == ph_user:
                matching_chars += 1
            elif j == 1 and ph_user in SIMILAR_JUNGSUNG_MAP.get(ph_correct, []):
                # Allow similar Jungsung phonemes to be considered correct
                matching_chars += 1
            else:
                mistaken_indices.append(i)
                if j != 2:  # Final consonant (Jongsung)
                    recommended_phonemes.append(ph_correct)
                else:
                    recommended_last_phonemes.append(ph_correct)

    # Calculate penalties for extra characters in the user's text
    if len(correct_text) < len(user_text):
        for j in range(i + 1, len(user_text)):
            penalties += 10
            mistaken_indices.append(j)

    # Calculate accuracy, ensuring it does not go below 0
    accuracy = int((matching_chars / total_chars) * 100) - penalties
    accuracy = max(accuracy, 0)
    
    # Special case: if accuracy is 100% but there are penalties, add '-1' to recommendations
    if int((matching_chars / total_chars) * 100) == 100 and penalties > 0:
        recommended_phonemes.append('-1')

    # Remove duplicates and irrelevant phonemes from recommendations
    mistaken_indices = list(set(mistaken_indices))
    recommended_phonemes = list(set(recommended_phonemes))
    recommended_last_phonemes = list(set(recommended_last_phonemes))

    recommended_phonemes = [phoneme for phoneme in recommended_phonemes if phoneme not in [' ', '*']]
    recommended_last_phonemes = [phoneme for phoneme in recommended_last_phonemes if phoneme not in [' ', '*']]

    return accuracy, mistaken_indices, recommended_phonemes, recommended_last_phonemes

def translate_korean_to_english(text):
    print(text)
    translator = Translator()
    translated = translator.translate(text, src='ko', dest='en')
    return translated.text

async def generate_eng_pronunciation(text):
    r = Romanizer(text)
    return r.romanize()
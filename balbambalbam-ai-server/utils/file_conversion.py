import base64
import tempfile

def base64_to_wav(base64_encoded_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav_data = base64.b64decode(base64_encoded_data)
        temp_file.write(wav_data)
        return temp_file.name

def file_to_base64(file):
    file.seek(0)
    data = file.read()
    base64_encoded_data = base64.b64encode(data).decode('utf-8')
    return base64_encoded_data
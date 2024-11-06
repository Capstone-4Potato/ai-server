import httpx
import argparse
import asyncio

def read_file_to_base64(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    return content.strip()

async def send_request_and_print_status(url, data, print_response=False):
    timeout = httpx.Timeout(15.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=data)
        print(f"Status Code for {url}: {response.status_code}")
        if print_response:
            print("Response Text:", response.text)

def get_test_data(endpoint):
    if endpoint == 'eng-pronunciation':
        return {'text': '아'}
    elif endpoint == 'eng-translation':
        return {'text': '아'}
    elif endpoint == 'kor-translation':
        return {'text': 'Hi'}
    elif endpoint == 'db-voice':
        return {
            'text': '몸 조리 잘 해',
        }
    elif endpoint == 'voice':
        return {
            'gender': 1,
            'age': 14,
            'text': '아',
        }
    elif endpoint == 'test':
        return {
            'userAudio' : read_file_to_base64('hello_wav_base64.txt'),
            'correctText' : '안녕'
        }
    elif endpoint == 'feedback':
        return {
            'userAudio' : read_file_to_base64('hello_wav_base64.txt'),
            'correctAudio' : read_file_to_base64('hello_wav_base64.txt'),
            'pronunciation' : '안녕'
        }
    elif endpoint == 'feedback_test':
        return {
            'userAudio' : read_file_to_base64('hello_wav_base64.txt'),
            'correctAudio' : read_file_to_base64('hello_wav_base64.txt'),
            'pronunciation' : '안녕'
        }
    else:
        raise ValueError(f"Unknown endpoint: {endpoint}")

async def test_all_endpoints(base_url, endpoints, print_response=False):
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            data = get_test_data(endpoint)
            await send_request_and_print_status(url, data, print_response)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test API endpoints.")
    parser.add_argument('endpoint', type=str, nargs='?', help='The endpoint to test, e.g., eng-pronunciation, eng-translation, etc. If omitted, all endpoints will be tested.')
    
    args = parser.parse_args()
    base_url = 'http://127.0.0.1:5000/ai/'
    endpoints = ['eng-pronunciation', 'eng-translation', 'kor-translation', 'db-voice', 'voice', 'test', 'feedback', 'feedback_test']

    if args.endpoint:
        if args.endpoint in endpoints:
            asyncio.run(test_all_endpoints(base_url, [args.endpoint], print_response=True))
        else:
            print(f"Unknown endpoint: {args.endpoint}")
    else: 
        asyncio.run(test_all_endpoints(base_url, endpoints))
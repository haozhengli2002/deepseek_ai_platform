import requests
import json
from flask import Response

def chat_with_model(data):
    prompt = data.get('prompt')
    response = requests.post('http://localhost:11434/api/generate', json={"model": "deepseek-r1:1.5b", "prompt": prompt})
    
    try:
        response_lines = response.text.strip().splitlines()
        # 使用 json.loads() 替代 eval()
        parsed_responses = [json.loads(line) for line in response_lines]
        final_text = ''.join(item['response'] for item in parsed_responses if 'response' in item)
        final_text = final_text.replace('<think>', '').replace('</think>', '').strip()
        return Response(final_text, mimetype='text/plain')
    except (json.JSONDecodeError, KeyError):
        return Response("Invalid JSON response from model", mimetype='text/plain')

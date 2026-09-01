import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.environ.get("SARVAM_API_KEY")

payload = {
    "inputs": ["దయచేసి 14 అంకెల ఆభా సంఖ్య నమోదు చేయండి."],
    "target_language_code": "te-IN",
    "speaker": "kavitha",
    "pitch": 0,
    "pace": 1.0,
    "loudness": 1.5,
    "speech_sample_rate": 8000,
    "enable_preprocessing": True,
    "model": "bulbul:v3"
}

headers = {
    "api-subscription-key": api_key,
    "Content-Type": "application/json"
}

res = requests.post("https://api.sarvam.ai/text-to-speech", json=payload, headers=headers)
print(res.status_code)
print(res.text[:500])

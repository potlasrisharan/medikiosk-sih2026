import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

headers = {"apikey": key, "Authorization": f"Bearer {key}"}
res = requests.get(f"{url}/rest/v1/encounters?limit=1", headers=headers)
print("Keys:", res.json()[0].keys() if res.json() else "Empty")

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "backend/.env"))

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

print("Tables in Supabase:")
try:
    res = supabase.table('patients').select('id').limit(1).execute()
    print("patients ok")
except Exception as e: print("patients fail:", e)

try:
    res = supabase.table('kiosk_settings').select('id').limit(1).execute()
    print("kiosk_settings ok")
except Exception as e: print("kiosk_settings fail:", e)


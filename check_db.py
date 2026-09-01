import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv("backend/.env")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

res = supabase.table('encounters').select('*').execute()
print("Total rows:", len(res.data))
for r in res.data:
    print(r.get('id'), r.get('token_number'), r.get('patient_name'), "has_ui_data:", r.get('ui_data') is not None)
    if r.get('ui_data'):
        print("   ui_data keys:", list(r.get('ui_data').keys()))
        print("   ui_data tokenNumber:", r.get('ui_data').get('tokenNumber'))

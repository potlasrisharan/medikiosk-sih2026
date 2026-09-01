import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "backend/.env"))

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

print("Adding columns to patients table...")
try:
    res = supabase.rpc('execute_sql', {'sql': 'ALTER TABLE patients ADD COLUMN IF NOT EXISTS preferred_language text DEFAULT \'en-IN\'; ALTER TABLE patients ADD COLUMN IF NOT EXISTS display_theme text DEFAULT \'light\';'}).execute()
    print("Columns added.", res)
except Exception as e:
    print("Error (RPC might not exist, but we will ignore if we can't alter it programmatically without psql):", e)

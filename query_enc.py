import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv("backend/.env")
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
print(supabase.table('encounters').select('*').limit(1).execute())

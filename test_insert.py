import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv("backend/.env")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

newEncounter = {
    "id": "enc-123456",
    "tokenNumber": "#045",
    "patientName": "Ramesh Chandra",
    "age": 52,
    "gender": "Male",
    "hasPmjay": True,
    "isEmergency": False,
    "nativeLang": "Telugu",
    "englishTranslation": "Knee pain",
    "subjective": "Bilateral knee pain"
}

try:
    res = supabase.table('encounters').insert([{
         "id": newEncounter["id"],
         "token_number": newEncounter["tokenNumber"],
         "patient_id": "91-4829-1029-4821",
         "patient_name": newEncounter["patientName"],
         "age": newEncounter["age"],
         "gender": newEncounter["gender"].upper(),
         "chief_complaint": newEncounter["englishTranslation"],
         "triage_priority": 'ROUTINE',
         "pmjay_eligible": True,
         "system_type": 'ALLOPATHIC',
         "status": 'WAITING',
         "language": newEncounter["nativeLang"],
         "ui_data": newEncounter
    }]).execute()
    print("Insert success:", res.data)
except Exception as e:
    print("Insert failed:", e)

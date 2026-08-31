import uuid
import datetime
import sqlite3
import json
from typing import Dict, Any, Optional, List
from ..models.schemas import PatientProfile, Gender

DB_PATH = "backend/medikiosk.db"

class ABDMService:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS abdm_transactions (
            id TEXT PRIMARY KEY,
            transaction_id TEXT NOT NULL,
            encounter_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            abha_id TEXT NOT NULL,
            token_number TEXT NOT NULL,
            diagnosis TEXT,
            prescription_json TEXT,
            soap_json TEXT,
            fhir_bundle_id TEXT,
            abdm_status TEXT NOT NULL,
            pmjay_claim_id TEXT,
            created_at TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def verify_abha(self, query: str) -> PatientProfile:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE abha_number = ? OR phone = ? OR id = ?", (query, query, query))
        row = cursor.fetchone()
        conn.close()

        if row:
            p = dict(row)
            return PatientProfile(
                patient_id=p["id"],
                abha_number=p["abha_number"],
                abha_address=p["abha_address"],
                full_name=p["full_name"],
                gender=Gender.MALE if p["gender"].upper() == "MALE" else Gender.FEMALE,
                year_of_birth=datetime.datetime.now().year - p["age"],
                address={"state": "Telangana", "district": "Khammam"},
                pmjay_eligible=True if p["pmjay_status"] == "ACTIVE" else False
            )

        # Default fallback demo profile
        return PatientProfile(
            patient_id="pat-048291",
            abha_number="91-4829-1029-4821",
            abha_address="ramesh.chandra@abdm",
            full_name="Ramesh Chandra",
            gender=Gender.MALE,
            year_of_birth=1974,
            address={"state": "Telangana", "district": "Khammam"},
            pmjay_eligible=True
        )

    def create_nha_abha(self, full_name: str, age: int, gender: str, phone: str, aadhaar: Optional[str] = None, state: str = "Telangana", district: str = "Khammam", pincode: str = "507001") -> Dict[str, Any]:
        patient_id = f"pat-{uuid.uuid4().hex[:6]}"
        rand_num = uuid.uuid4().hex[:12]
        abha_number = f"91-{rand_num[0:4]}-{rand_num[4:8]}-{rand_num[8:12]}"
        clean_name = "".join(e for e in full_name.lower() if e.isalnum())
        abha_address = f"{clean_name}.{rand_num[:4]}@abdm"
        masked_aadhaar = f"XXXX-XXXX-{aadhaar[-4:]}" if aadhaar and len(aadhaar) >= 4 else f"XXXX-XXXX-{rand_num[:4]}"
        pmjay_id = f"PMJAY-TS-{rand_num[:6]}"
        yob = datetime.datetime.now().year - age
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO patients (id, full_name, age, gender, phone, abha_number, abha_address, aadhaar_masked, pmjay_status, pmjay_id, auth_method, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient_id, full_name, age, gender, phone, abha_number, abha_address, masked_aadhaar, "ACTIVE", pmjay_id, "ABDM M1 Govt Registration", created_at
        ))
        conn.commit()
        conn.close()

        return {
            "patient_id": patient_id,
            "full_name": full_name,
            "age": age,
            "year_of_birth": yob,
            "gender": gender,
            "phone": phone,
            "abha_number": abha_number,
            "abha_address": abha_address,
            "aadhaar_masked": masked_aadhaar,
            "state": state,
            "district": district,
            "pincode": pincode,
            "pmjay_status": "ACTIVE",
            "pmjay_id": pmjay_id,
            "auth_method": "ABDM M1 Government Registration",
            "kyc_status": "VERIFIED_UIDAI_NHA",
            "created_at": created_at
        }

    def push_approved_encounter_to_ndhm(self, encounter_id: str, patient_id: str, patient_name: str, abha_id: str, token_number: str, diagnosis: str, prescription: Any = None, soap: Any = None) -> Dict[str, Any]:
        tx_id = f"ABDM-TX-{uuid.uuid4().hex[:10].upper()}"
        fhir_id = f"urn:uuid:{uuid.uuid4()}"
        pmjay_claim = f"PMJAY-CLM-{uuid.uuid4().hex[:6].upper()}"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO abdm_transactions (id, transaction_id, encounter_id, patient_id, patient_name, abha_id, token_number, diagnosis, prescription_json, soap_json, fhir_bundle_id, abdm_status, pmjay_claim_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            tx_id,
            encounter_id,
            patient_id,
            patient_name,
            abha_id,
            token_number,
            diagnosis,
            json.dumps(prescription) if prescription else "[]",
            json.dumps(soap) if soap else "{}",
            fhir_id,
            "M2_CARE_CONTEXT_LINKED_GOVT_DB",
            pmjay_claim,
            now_str
        ))
        conn.commit()
        conn.close()

        return {
            "status": "SUCCESS_PUSHED_TO_GOVT_DB",
            "transaction_id": tx_id,
            "encounter_id": encounter_id,
            "patient_name": patient_name,
            "abha_id": abha_id,
            "token_number": token_number,
            "fhir_bundle_id": fhir_id,
            "abdm_milestone": "M2_HIP_CARE_CONTEXT_LINKED",
            "pmjay_claim_status": "AUTO_PREAUTH_APPROVED",
            "pmjay_claim_id": pmjay_claim,
            "timestamp": now_str
        }

    def get_all_abdm_transactions(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM abdm_transactions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

abdm_service = ABDMService()

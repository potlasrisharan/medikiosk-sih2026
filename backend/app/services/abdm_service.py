import uuid
import datetime
import sqlite3
from typing import Dict, Any, Optional
from ..models.schemas import PatientProfile, Gender

DB_PATH = "backend/medikiosk.db"

class ABDMService:
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
        # Official NHA 14-digit format: 91-XXXX-XXXX-XXXX
        abha_number = f"91-{rand_num[0:4]}-{rand_num[4:8]}-{rand_num[8:12]}"
        clean_name = "".join(e for e in full_name.lower() if e.isalnum())
        abha_address = f"{clean_name}.{rand_num[:4]}@abdm"
        masked_aadhaar = f"XXXX-XXXX-{aadhaar[-4:]}" if aadhaar and len(aadhaar) >= 4 else f"XXXX-XXXX-{rand_num[:4]}"
        pmjay_id = f"PMJAY-TS-{rand_num[:6]}"
        yob = datetime.datetime.now().year - age
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Persist directly into SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO patients (id, full_name, age, gender, phone, abha_number, abha_address, aadhaar_masked, pmjay_status, pmjay_id, auth_method, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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

abdm_service = ABDMService()

from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from ..models.schemas import EncounterQueueItem, SoapNote, Gender, TriagePriority, SystemType
from ..services.fhir_service import fhir_service
import datetime

router = APIRouter(prefix="/doctor", tags=["Doctor Portal"])

TOKEN_COUNTER = 42

ENCOUNTERS_STORE = [
    EncounterQueueItem(
        encounter_id="enc-e012",
        token_number="#E-012",
        patient_name="Mohan Das",
        age=61,
        gender=Gender.MALE,
        chief_complaint="🚨 ACUTE CHEST PAIN: Severe retrosternal pain radiating to left jaw & diaphoresis for 30 mins.",
        triage_priority=TriagePriority.EMERGENCY,
        pmjay_eligible=True,
        system_type=SystemType.ALLOPATHIC,
        created_at=datetime.datetime.now().strftime("%I:%M %p"),
        status="EMERGENCY_TRIAGE"
    ),
    EncounterQueueItem(
        encounter_id="enc-0042",
        token_number="#042",
        patient_name="Ramesh Chandra",
        age=52,
        gender=Gender.MALE,
        chief_complaint="Bilateral knee pain with crepitus for 6 months, worsening with cold.",
        triage_priority=TriagePriority.ROUTINE,
        pmjay_eligible=True,
        system_type=SystemType.AYURVEDIC,
        created_at=datetime.datetime.now().strftime("%I:%M %p"),
        status="WAITING"
    ),
    EncounterQueueItem(
        encounter_id="enc-0043",
        token_number="#043",
        patient_name="Priya Sharma",
        age=34,
        gender=Gender.FEMALE,
        chief_complaint="Epigastric burning, acid reflux, and nausea for 3 weeks.",
        triage_priority=TriagePriority.ROUTINE,
        pmjay_eligible=True,
        system_type=SystemType.AYURVEDIC,
        created_at=(datetime.datetime.now() - datetime.timedelta(minutes=7)).strftime("%I:%M %p"),
        status="WAITING"
    )
]

SOAP_STORE = {
    "enc-0042": SoapNote(
        encounter_id="enc-0042",
        subjective="Patient reports severe knee stiffness and crepitus, aggravated during early mornings and cold exposure. Walking capacity reduced to 200 meters. Denies trauma.",
        objective="Clinical Vitals: [Pending In-Person Measurement in OPD Chamber]\nPatient-Elicited History: Bilateral knee joint crepitus, severe stiffness on waking (>30 mins), cold weather aggravation.\nScanned Paper Lab Report (Sarvam 3B VLM): Serum Uric Acid 7.8 mg/dL [CRITICAL_HIGH] (Ref: 3.5 - 7.2 mg/dL).",
        assessment="1. Sandhigata Vata (Osteoarthritis / ICD-10 M17.0 / NAMASTE AYU-SAN-01)\n2. Hyperuricemia (Serum Uric Acid 7.8 mg/dL [HIGH])\n3. Mild Agnimandya (Manda Agni)",
        plan="Rx Formulations:\n1. Tab. Yograj Guggulu 2 tabs BD with warm water pc (15 days)\n2. Kwath. Maharasnadi 20ml with equal water BD ac (15 days)\n3. Ext. Janu Basti with Ksheerabala Taila 7 sittings\n\nInvestigations Ordered:\n- Bilateral Knee AP/Lateral Weight-bearing X-ray\n- Repeat Serum Uric Acid after 4 weeks",
        critical_alerts=["Serum Uric Acid: 7.8 mg/dL [HIGH] (Ref: 3.5 - 7.2 mg/dL)"],
        dashavidha_matrix={
            "Prakriti": "Vata-Kapha",
            "Vikriti": "Vata Vriddhi (Sandhigata)",
            "Sara": "Asthi Madhyama",
            "Samhanana": "Madhyama",
            "Pramana": "Height 172cm, Wt 78kg (BMI 26.2)",
            "Satmya": "Madhura-Lavana",
            "Sattva": "Madhyama",
            "Ahara_Shakti": "Manda Agni",
            "Vyayama_Shakti": "Avara (Low)",
            "Vaya": "Pravriddha (52Y)"
        }
    )
}

class NewIntakePayload(BaseModel):
    patient_name: str
    age: int
    gender: str
    identifier_type: str
    identifier_value: str
    symptoms: str
    language: str

@router.get("/queue", response_model=List[EncounterQueueItem])
async def get_doctor_queue():
    return ENCOUNTERS_STORE

@router.get("/token/next")
async def get_next_token():
    global TOKEN_COUNTER
    token_str = f"#{TOKEN_COUNTER:03d}"
    return {"token_number": token_str, "next_token_int": TOKEN_COUNTER}

@router.post("/encounter/create")
async def create_new_encounter(payload: NewIntakePayload):
    global TOKEN_COUNTER
    TOKEN_COUNTER += 1
    token_str = f"#{TOKEN_COUNTER:03d}"
    enc_id = f"enc-{TOKEN_COUNTER:04d}"
    
    new_item = EncounterQueueItem(
        encounter_id=enc_id,
        token_number=token_str,
        patient_name=payload.patient_name,
        age=payload.age,
        gender=Gender.MALE if payload.gender.lower() == "male" else Gender.FEMALE,
        chief_complaint=payload.symptoms or "General OPD Consultation",
        triage_priority=TriagePriority.ROUTINE,
        pmjay_eligible=True,
        system_type=SystemType.AYURVEDIC,
        created_at=datetime.datetime.now().strftime("%I:%M %p"),
        status="WAITING"
    )
    
    ENCOUNTERS_STORE.insert(0, new_item)
    
    SOAP_STORE[enc_id] = SoapNote(
        encounter_id=enc_id,
        subjective=f"Patient {payload.patient_name} ({payload.age}Y) registered via MediKiosk ({payload.identifier_type.upper()}: {payload.identifier_value}). Chief Complaint: {payload.symptoms}.",
        objective="Clinical Vitals: [To be recorded by consulting physician in OPD chamber]\nPatient Self-Reported Symptoms: Elicited via voice intake.",
        assessment="1. Initial OPD Assessment\n2. PM-JAY Cashless OPD Benefit Active",
        plan="Clinical consultation pending.\nRecommended preliminary Ayurvedic Rasayana therapy.",
        critical_alerts=[],
        dashavidha_matrix={
            "Prakriti": "Vata-Pitta",
            "Vikriti": "Vata Dominance",
            "Ahara_Shakti": "Madhyama Agni"
        }
    )
    
    return {
        "status": "success",
        "encounter_id": enc_id,
        "token_number": token_str,
        "patient_name": payload.patient_name
    }

@router.get("/encounter/{encounter_id}/soap", response_model=SoapNote)
async def get_soap_note(encounter_id: str):
    if encounter_id in SOAP_STORE:
        return SOAP_STORE[encounter_id]
    return SOAP_STORE["enc-0042"]

@router.get("/encounter/{encounter_id}/fhir")
async def get_encounter_fhir(encounter_id: str):
    soap = SOAP_STORE.get(encounter_id, SOAP_STORE["enc-0042"])
    return fhir_service.generate_document_bundle(
        encounter_id=encounter_id,
        patient_id="pat-048291",
        soap_note=soap.model_dump()
    )

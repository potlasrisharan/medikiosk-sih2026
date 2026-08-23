from fastapi import APIRouter
from typing import List
from ..models.schemas import EncounterQueueItem, SoapNote, Gender, TriagePriority, SystemType
from ..services.fhir_service import fhir_service

router = APIRouter(prefix="/doctor", tags=["Doctor Portal"])

ENCOUNTERS_STORE = [
    EncounterQueueItem(
        encounter_id="enc-0042",
        token_number="#042",
        patient_name="Ramesh Chandra",
        age=52,
        gender=Gender.MALE,
        chief_complaint="Bilateral knee pain with crepitus for 6 months, worsening with cold.",
        triage_priority=TriagePriority.ROUTINE,
        pmjay_eligible=True,
        system_type=SystemType.HYBRID,
        created_at="10:30 AM",
        status="WAITING"
    ),
    EncounterQueueItem(
        encounter_id="enc-0043",
        token_number="#043",
        patient_name="Lakshmi Devi",
        age=48,
        gender=Gender.FEMALE,
        chief_complaint="Chronic acid peptic disorder (Amlapitta), burning sensation in epigastrium.",
        triage_priority=TriagePriority.ROUTINE,
        pmjay_eligible=True,
        system_type=SystemType.AYURVEDIC,
        created_at="10:35 AM",
        status="WAITING"
    )
]

@router.get("/queue", response_model=List[EncounterQueueItem])
async def get_queue():
    return ENCOUNTERS_STORE

@router.get("/encounter/{encounter_id}/soap", response_model=SoapNote)
async def get_encounter_soap(encounter_id: str):
    return SoapNote(
        subjective="52-year-old male presents with bilateral knee pain for 6 months, aggravated by walking and cold weather. Morning stiffness lasting ~20 mins. History of Hypertension for 3 years on Telmisartan 40mg. No known drug allergies.",
        objective="Vitals: BP 130/84 mmHg, Pulse 76 bpm. Musculoskeletal: Bilateral knee joint crepitus present, no active effusion. Lab Findings: Serum Uric Acid: 7.8 mg/dL [HIGH], HbA1c: 6.1%.",
        assessment="1. Osteoarthritis Bilateral Knees (Sandhigata Vata) with mild hyperuricemia. 2. Essential Hypertension (Controlled).",
        plan="1. Continue Telmisartan 40mg OD. 2. Yograj Guggulu 2 tabs BD after food. 3. Janu Basti / Local fomentation advised. 4. Low purine diet counselled. Review in 3 weeks.",
        dashavidha_summary={
            "Prakriti": "Vata-Kapha",
            "Vikriti": "Vata (Dhatu Kshaya / Sandhigata)",
            "Agni": "Manda Agni",
            "Koshtha": "Madhyama Koshtha"
        },
        pmjay_status="Active (₹5,00,000 Annual Coverage - Cashless Approved)",
        triage_priority=TriagePriority.ROUTINE
    )

@router.get("/encounter/{encounter_id}/fhir")
async def get_fhir_bundle(encounter_id: str):
    soap = await get_encounter_soap(encounter_id)
    return fhir_service.generate_document_bundle(encounter_id, "pat-048291", soap.dict())

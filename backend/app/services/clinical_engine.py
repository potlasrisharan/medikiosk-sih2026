import time
import re
from typing import Tuple, List, Dict, Any
from ..models.schemas import RedFlagAlert, SystemType, TriagePriority

RED_FLAG_PATTERNS = [
    r"chest pain", r"severe chest", r"left arm pain", r"heart attack",
    r"chhaati mein dard", r"seene mein dard", r"tez dard",
    r"shortness of breath", r"breathless", r"saans lene mein takleef",
    r"fainting", r"unconscious", r"behosh", r"blood in vomit", r"khoon ki ulti",
    r"sudden paralysis", r"slurred speech", r"face drooping", r"stroke"
]

ALLOPATHIC_QUESTIONS = [
    "Aapko yeh takleef kab se hai? (Duration / Onset)",
    "Dard ya takleef kis jagah par zyada mehsoos hoti hai? (Site / Location)",
    "Dard kaisa mehsoos hota hai - chubhne jaisa, jalan, ya dukhne jaisa? (Character)",
    "Kya dard kisi aur hisse mein bhi failta hai? (Radiation)",
    "Iske sath bukhar, chakkar ya ulti jaisa kuch lag raha hai? (Associated Symptoms)",
    "Kya kisi dawai ya khane se allergy hai? (Allergies)"
]

DASHVAIDHA_QUESTIONS = [
    "Aapki bhookh (Agni) kaisi hai - achhi, kamzor, ya aniyamit?",
    "Aapka pet (Koshtha / Bowel) theek saaf hota hai?",
    "Aapko neend aur thakaan (Nidra / Bala) kaisa rehta hai?",
    "Aapko sardi ya garmi mein se kisme zyada pareshani hoti hai (Prakriti / Sheeta-Ushna)?"
]

class ClinicalIntelligenceEngine:
    def evaluate_red_flag(self, text: str) -> RedFlagAlert:
        start_time = time.perf_counter()
        normalized_text = text.lower()
        matched = []
        for pattern in RED_FLAG_PATTERNS:
            if re.search(pattern, normalized_text):
                matched.append(pattern)
        
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        
        if matched:
            return RedFlagAlert(
                is_triggered=True,
                trigger_symptoms=matched,
                recommended_action="EMERGENCY_TRIAGE_ALERT",
                latency_ms=round(latency_ms, 2)
            )
        return RedFlagAlert(
            is_triggered=False,
            trigger_symptoms=[],
            recommended_action="PROCEED_WITH_INTAKE",
            latency_ms=round(latency_ms, 2)
        )

    def generate_next_prompt(self, current_input: str, step_index: int, system_type: SystemType) -> Tuple[str, List[str], bool]:
        if system_type == SystemType.AYURVEDIC:
            q_list = DASHVAIDHA_QUESTIONS
        elif system_type == SystemType.ALLOPATHIC:
            q_list = ALLOPATHIC_QUESTIONS
        else:
            q_list = ALLOPATHIC_QUESTIONS + DASHVAIDHA_QUESTIONS

        if step_index < len(q_list):
            next_q = q_list[step_index]
            options = ["Haan, bilkul", "Nahi, aisi koi baat nahi", "Thoda bohot", "Pehle se behtar"]
            return next_q, options, False
        else:
            return "Dhanyawad. Aapka complete clinical case record taiyyar ho gaya hai.", ["Review Summary"], True

clinical_engine = ClinicalIntelligenceEngine()

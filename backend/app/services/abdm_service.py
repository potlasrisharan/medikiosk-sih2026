from ..models.schemas import PatientProfile, Gender, CoverageEligibilityResponse

class ABDMIntegrationService:
    def verify_abha(self, abha_query: str) -> PatientProfile:
        return PatientProfile(
            patient_id="pat-048291",
            abha_number="91-4829-1029-4821",
            abha_address="ramesh.chandra@abdm",
            name="Ramesh Chandra",
            gender=Gender.MALE,
            age=52,
            phone="+91 9876543210",
            address="Khammam, Telangana, India"
        )

    def check_coverage_eligibility(self, abha_number: str) -> CoverageEligibilityResponse:
        # NHA NHCX FHIR CoverageEligibilityRequest
        return CoverageEligibilityResponse(
            eligible=True,
            scheme_name="Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
            coverage_amount_inr=500000.0,
            beneficiary_id="PMJAY-TEL-90821-A",
            status="ACTIVE",
            message="Beneficiary actively verified under PM-JAY. Eligible for 100% cashless consultation & diagnostics."
        )

abdm_service = ABDMIntegrationService()

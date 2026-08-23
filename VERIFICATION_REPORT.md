# 🔍 MediKiosk Documentation Suite — Phase 1 Comprehensive Verification Report

**Execution Timestamp:** 2026-08-23T18:40:00+05:30  
**Target:** SIH Problem Statement 26047 Documentation Suite (`docs/` & root)  
**Status:** Verification Completed  

---

## 1. Executive Summary of Findings

| Item # | Category | Claim / Entity Checked | Verified Source Used | Verdict | Key Finding / Action Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1.1** | **ABDM / NHA** | `find-benefit-program` endpoint | `abdm.gov.in`, `sandbox.abdm.gov.in` | ❌ **INCORRECT / NON-EXISTENT** | No such endpoint exists in ABDM Sandbox. Real NHA/NRCeS mechanism for PM-JAY & insurance eligibility is **NHCX `CoverageEligibilityRequest`** (FHIR R4) and PM-JAY Beneficiary Identification System (BIS). Must replace/reframe accordingly. |
| **1.2** | **ABDM / NHA** | ABDM v0.5 M3 Consent & Data Flow endpoints | `NHA-ABDM/ABDM-wrapper`, `sandbox.abdm.gov.in` | ✅ **CONFIRMED** | `/v0.5/consent-requests/init`, `/on-init`, `/consents/hiu/notify`, `/on-notify`, `/consents/fetch`, `/on-fetch`, `/health-information/hiu/request`, `/transfer` match official NHA specs. |
| **1.3** | **ABDM / NHA** | ABDM M3_V1 Sandbox Doc | `sandbox.abdm.gov.in` | ✅ **CONFIRMED** | M3_V1 is the official milestone specification for HIU consent and health data exchange. |
| **2.1** | **NRCeS / FHIR** | `bdl-11` Invariant (`DocumentBundle` first entry `Composition`) | `hl7.org/fhir/R4/bundle.html`, `nrces.in/ndhm/fhir/r4/` | ✅ **CONFIRMED** | `bdl-11` is the official invariant: `type = 'document' implies entry.first().resource.is(Composition)`. Enforced strictly by NRCeS India. |
| **2.2** | **NRCeS / FHIR** | NRCeS FHIR R4 Implementation Guide | `https://nrces.in/ndhm/fhir/r4/` | ✅ **CONFIRMED** | Active Indian national FHIR R4 standard maintained by NRCeS / MoHFW. |
| **3.1** | **Sarvam AI** | Language counts: Saaras, Bulbul, Document Digitisation | `sarvam.ai`, `docs.sarvam.ai` | ⚠️ **PARTIALLY INCORRECT** | **Saaras (STT):** 22 Indian languages + English (23 total). **Bulbul (TTS):** 11 languages (10 Indian + English, 35+ voices). **Document Digitisation (Vision 3B):** 22 Indian + English (23 total). Blanket "22 languages for all three" must be corrected. |
| **3.2** | **Sarvam AI** | Model names & Python SDK | `docs.sarvam.ai`, PyPI `sarvamai` | ✅ **CONFIRMED** | Official SDK is `sarvamai`, client `SarvamAI`, models `saaras:v3`, `bulbul:v3`, and Sarvam Vision 3B. |
| **4.1** | **Eka Care** | Eka Developer Platform Base URL & Auth Flow | `developer.eka.care` | ✅ **CONFIRMED** | Eka Console issues `client_id` and `client_secret` to obtain Bearer tokens; webhooks `abha.link_care_context` and `abha.hiu_data_push` manage ABDM callbacks. |
| **5.1** | **Academic Citation** | Irving et al. 2017 BMJ Open DOI | `bmjopen.bmj.com`, `PubMed` | ❌ **INCORRECT** | Document cited `10.1136/bmjopen-2017-017982`. Correct DOI is **`10.1136/bmjopen-2017-017902`**. Must fix across all 8 files. |
| **5.2** | **Academic Citation** | Hampton et al. 1975 BMJ (70-80% diagnostic reliance) | `bmj.com`, `PubMed` | ✅ **CONFIRMED** | DOI `10.1136/bmj.2.5969.486` confirmed. 66/80 (82.5%) patients accurately diagnosed from history alone. |
| **5.3** | **Clinical Citation** | *Charaka Samhita* Vimana Sthana 8:94-130 | *Rogabhishagjitiya Vimana Adhyaya* | ✅ **CONFIRMED** | Exact classical locus for the 10-fold *Dashavidha Pariksha* (*Prakriti, Vikriti, Sara, Samhanana, Pramana, Satmya, Satva, Ahara Shakti, Vyayama Shakti, Vaya*). |
| **5.4** | **Legal Citation** | DPDPA 2023 Gazette & MeitY URL | `meity.gov.in`, Gazette of India | ✅ **CONFIRMED** | Act No. 22 of 2023, published August 11, 2023. |
| **6.1** | **Consistency** | Endpoints in 02 mapped to tables in 03 | Cross-file audit | ⚠️ **DISCREPANCY** | `departments`, `facilities`, and `practitioners` tables had no explicit registration endpoints in 02 (admin/master data). Added documentation note. |
| **6.2** | **Consistency** | 5-Step Journey alignment across 01, 02, 04, 06 | Cross-file audit | ✅ **CONFIRMED** | Step names and sequence: Step 1 (Identify), Step 2 (Converse), Step 3 (Scan), Step 4 (Summarize & Route), Step 5 (Consult). |
| **7.1** | **SQL Syntax** | PostgreSQL 16 DDL syntax in `03_DATABASE_SCHEMA_AND_ERD.sql` | PostgreSQL 16 Parser | ❌ **SYNTAX ERRORS DETECTED** | Unquoted ENUM literals and unquoted VARCHAR/ENUM `DEFAULT` strings in DDL schema will fail on PostgreSQL 16. Must enclose in single quotes. |
| **7.2** | **YAML Syntax** | Docker Compose & GitHub Actions in `05_DEVOPS_CICD_AND_DEPLOYMENT.md` | YAML Linter | ✅ **CONFIRMED** | Valid YAML syntax. |
| **7.3** | **JSON Syntax** | 12 JSON code blocks across 02 & 04 | Python `json.loads` | ✅ **CONFIRMED** | All 12 JSON code blocks parsed with zero errors. |

---

## 2. Detailed Verification Notes

### 2.1 ABDM Benefit Discovery vs. NHCX & PM-JAY BIS
* **Finding:** The endpoint `find-benefit-program` was previously assumed to be an ABDM V3 REST endpoint. Thorough inspection of `abdm.gov.in`, `sandbox.abdm.gov.in`, and NHA press releases confirms that ABDM V3 does not expose a standalone `find-benefit-program` endpoint.
* **Official Reality:** In the Indian national digital health stack, health insurance and scheme entitlements (such as PM-JAY and state health schemes) are governed through:
  1. **National Health Claims Exchange (NHCX):** Operates on NRCeS FHIR R4 profiles using `CoverageEligibilityRequest` (and `CoverageEligibilityRequestBundle`) to query payers/TPAs and returns `CoverageEligibilityResponse`.
  2. **PM-JAY Beneficiary Identification System (BIS):** NHA's national portal and API for verifying Ayushman Card (Golden Card) / PM-JAY family eligibility using Ration Card, Aadhaar, or PM-JAY ID.
* **Resolution:** Reframe the benefit check in MediKiosk as the **NHCX FHIR R4 Coverage Eligibility & PM-JAY BIS Verification Engine**, detailing the real `CoverageEligibilityRequest` FHIR payload.

### 2.2 Sarvam AI Precise Language Breakdown
* **Finding:** Sarvam AI does not support 22 languages uniformly across all modalities.
* **Official Specs:**
  * **Saaras v3 (Speech-to-Text):** 22 Indian languages + English (23 languages total).
  * **Bulbul v3 (Text-to-Speech):** 11 languages (Hindi, English, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu) with 35+ expressive voices.
  * **Sarvam Vision (Document Digitisation 3B VLM):** 22 Indian languages + English (23 languages total).
* **Resolution:** Update all 8 documents to clearly differentiate STT/OCR (23 languages) from TTS (11 languages).

### 2.3 Academic Citation: Irving et al. (2017) DOI Error
* **Finding:** The DOI was recorded as `10.1136/bmjopen-2017-017982`.
* **Official DOI:** `10.1136/bmjopen-2017-017902` (BMJ Open, Vol 7, Issue 10, e017902).
* **Resolution:** Update every occurrence in `01_PRODUCT_REQUIREMENTS_DOCUMENT.md`, `07_REFERENCES_AND_CITATIONS.md`, and `README.md`.

### 2.4 SQL Syntax: PostgreSQL 16 DDL Parser Validation
* **Finding:** ENUM definitions and DEFAULT constraints used unquoted strings (e.g. `CREATE TYPE gender_enum AS ENUM (MALE, FEMALE...);` and `DEFAULT AYUSH_ALLOPATHIC_HYBRID`).
* **Resolution:** Properly wrap all string literals in single quotes (e.g. `CREATE TYPE gender_enum AS ENUM ('MALE', 'FEMALE'...);` and `DEFAULT 'AYUSH_ALLOPATHIC_HYBRID'`).

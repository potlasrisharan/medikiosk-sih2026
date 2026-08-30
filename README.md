# 🏥 MediKiosk Documentation Suite

Welcome to the comprehensive engineering documentation for **MediKiosk**, the AI-Powered Multimodal Clinical Intake & ABDM Digitization Platform for Smart India Hackathon 2026 (Problem Statement ID: `26047`, Ministry of Ayush / AIIA).

---

## 📂 Documentation Suite Index

All master technical specifications and submission decks are maintained in the structured [`/docs`](./docs) directory:

| Document | Title & Core Specification | Primary Standards & Integrations |
| :--- | :--- | :--- |
| **[`docs/01_PRODUCT_REQUIREMENTS_DOCUMENT.md`](./docs/01_PRODUCT_REQUIREMENTS_DOCUMENT.md)** | Master Product Requirements Document | BMJ Open 2017 ([DOI: 10.1136/bmjopen-2017-017902](https://doi.org/10.1136/bmjopen-2017-017902)), 5-Step Journey, SOCRATES & *Dashavidha Pariksha* Ontologies |
| **[`docs/02_SYSTEM_ARCHITECTURE_AND_APIS.md`](./docs/02_SYSTEM_ARCHITECTURE_AND_APIS.md)** | High-Level System Architecture & API Specs | Flutter Kiosk, Next.js 15, FastAPI, [Sarvam AI APIs](https://www.sarvam.ai/), [Eka Care ABDM APIs](https://developer.eka.care/) |
| **[`docs/03_DATABASE_SCHEMA_AND_ERD.sql`](./docs/03_DATABASE_SCHEMA_AND_ERD.sql)** | Production PostgreSQL 16 DDL & ERD | Supabase Managed PostgreSQL 16 (Validated Syntax), PostGIS, Row Level Security (RLS) |
| **[`docs/04_ABDM_FHIR_AND_SECURITY_SPEC.md`](./docs/04_ABDM_FHIR_AND_SECURITY_SPEC.md)** | ABDM, FHIR R4, M3_V1, NHCX & Security Spec | [NHA ABDM Sandbox](https://sandbox.abdm.gov.in/), [NRCeS FHIR R4 (bdl-11 Invariant)](https://nrces.in/ndhm/fhir/r4/), NHCX Eligibility, DPDPA 2023 |
| **[`docs/05_DEVOPS_CICD_AND_DEPLOYMENT.md`](./docs/05_DEVOPS_CICD_AND_DEPLOYMENT.md)** | Containerization, CI/CD & Deployment | Docker Compose Cluster, Multi-Stage Dockerfiles, GitHub Actions CI/CD Pipeline |
| **[`docs/06_SIH_PITCH_DECK_AND_DEMO_SCRIPT.md`](./docs/06_SIH_PITCH_DECK_AND_DEMO_SCRIPT.md)** | SIH 5-Slide Pitch Deck & 2-Min Live Demo | Grand Finale 5-Slide Deck, 120-Second Timed Script, Jury Defense Strategy |
| **[`docs/07_REFERENCES_AND_CITATIONS.md`](./docs/07_REFERENCES_AND_CITATIONS.md)** | Master Academic, Legal & Technical Citations | BMJ Open (DOI: 10.1136/bmjopen-2017-017902), BMJ (DOI: 10.1136/bmj.2.5969.486), Charaka Samhita, DPDPA 2023 Gazette |
| **[`docs/08_TECH_STACK_AND_COMPATIBILITY.md`](./docs/08_TECH_STACK_AND_COMPATIBILITY.md)** | Production Tech Stack & Compatibility Matrix | Full stack specifications, versions, package manifests, and latency budgets |
| **[`docs/MediKiosk_SIH2026_Idea_Submission.pdf`](./docs/MediKiosk_SIH2026_Idea_Submission.pdf)** | Official SIH Idea Presentation Deck (PDF) | Full 6-slide official submission format |

---

## 🏛️ Foundational Technology Stack

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    100% SOVEREIGN INDIAN STACK                                   │
├──────────────────────────────────────────┬───────────────────────────────────────────────────────┤
│    SARVAM AI SOVEREIGN INTELLIGENCE      │           NATIONAL ABDM, NHCX & EKA GATEWAYS          │
├──────────────────────────────────────────┼───────────────────────────────────────────────────────┤
│ • Saaras v3: 23 Language STT (22 Indic)  │ • ABDM Milestone 1 (M1): ABHA Verification / QR Scan  │
│ • Bulbul v3: 11 Language Regional TTS    │ • NHCX / PM-JAY: CoverageEligibilityRequest (FHIR)    │
│ • Sarvam Vision: 3B Medical VLM (23 Lang)│ • ABDM Milestone 2 (M2 - HIP): Care Context Linking   │
│ • Sarvam Translate: Multi-Language Norm  │ • ABDM Milestone 3 (M3 - HIU): Past FHIR Record Pull  │
└──────────────────────────────────────────┴───────────────────────────────────────────────────────┘
```

---

*Author: **Potla Sri Sharan** | Ministry of Ayush / All India Institute of Ayurveda (AIIA)*

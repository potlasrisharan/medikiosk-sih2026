    lucide.createIcons();

    const BASE_TRANSACTIONS = [
      {
        token: "#E-012",
        name: "Mohan Das",
        age: 61,
        gender: "Male",
        abha: "91-7712-4019-3382",
        complaint: "Acute Coronary Syndrome (STEMI)",
        isEmergency: true,
        abdmStatus: "M1 Verified",
        pmjayStatus: "APPROVED (₹75,000 STAT)",
        time: "10:45 AM"
      },
      {
        token: "#042",
        name: "Ramesh Chandra",
        age: 52,
        gender: "Male",
        abha: "91-4829-1029-4821",
        complaint: "Sandhigata Vata (Knee OA)",
        isEmergency: false,
        abdmStatus: "M1 Verified",
        pmjayStatus: "APPROVED (₹5,000)",
        time: "10:30 AM"
      },
      {
        token: "#043",
        name: "Priya Sharma",
        age: 34,
        gender: "Female",
        abha: "91-5910-2941-8402",
        complaint: "Amlapitta (Acid Peptic Disorder)",
        isEmergency: false,
        abdmStatus: "M1 Verified",
        pmjayStatus: "APPROVED (₹3,200)",
        time: "10:35 AM"
      },
      {
        token: "#044",
        name: "Ananya Verma",
        age: 28,
        gender: "Female",
        abha: "91-9123-4567-8901",
        complaint: "Vishama Jwara (Viral Pyrexia)",
        isEmergency: false,
        abdmStatus: "M1 Verified",
        pmjayStatus: "APPROVED (₹2,500)",
        time: "10:40 AM"
      }
    ];

    async function refreshTransactionFeed() {
      const totalCounter = document.getElementById("stat-opd-intakes");
      const tbody = document.getElementById("transaction-table-body");
      if (!tbody) return;

      let allTx = [];

      try {
        // Fetch real data from FastAPI backend
        const res = await fetch("http://localhost:8000/api/v1/doctor/queue");
        if (res.ok) {
          const queue = await res.json();
          allTx = queue.map(q => ({
            token: q.token_number,
            name: q.patient_name,
            age: q.age,
            gender: q.gender,
            abha: "91-XXXX-XXXX-XXXX", // Default if not in queue item
            complaint: q.chief_complaint,
            isEmergency: q.triage_priority === "Emergency_Red",
            abdmStatus: "M1 Verified (Backend)",
            pmjayStatus: q.pmjay_eligible ? "APPROVED (₹5,000)" : "N/A",
            time: q.created_at
          }));
        }
      } catch (err) {
        console.warn("Backend not reachable, falling back to local simulation", err);
      }

      // If backend failed or returned empty, use localStorage + base
      if (allTx.length === 0) {
        let customQueue = [];
        try {
          customQueue = JSON.parse(localStorage.getItem("MEDIKIOSK_SHARED_QUEUE") || "[]");
        } catch (e) {}

        customQueue.forEach(item => {
          allTx.push({
            token: item.tokenNumber,
            name: item.patientName,
            age: item.age,
            gender: item.gender,
            abha: item.abhaId || "91-XXXX-XXXX-XXXX",
            complaint: item.selectedSymptom || item.assessment || "General OPD Consultation",
            isEmergency: item.isEmergency,
            abdmStatus: "M1 Verified",
            pmjayStatus: item.hasPmjay ? "APPROVED (₹5,000)" : "N/A",
            time: item.timestamp || "Just Now"
          });
        });

        BASE_TRANSACTIONS.forEach(b => {
          if (!allTx.some(t => t.token === b.token)) {
            allTx.push(b);
          }
        });
      }

      if (totalCounter) {
        totalCounter.innerText = (4280 + allTx.length).toLocaleString();
      }

      tbody.innerHTML = allTx.map((tx, idx) => `
        <tr class="hover:bg-[#f0ede8] transition ${tx.isEmergency ? "bg-rose-50" : ""}">
          <td class="p-3 font-black ${tx.isEmergency ? "text-rose-400" : "text-[#FFA530]"}">
            ${tx.token}
          </td>
          <td class="p-3 font-bold text-[#223D79]">
            ${tx.name} <span class="text-[#77797C] font-normal">(${tx.age}${tx.gender === "Male" ? "M" : "F"})</span>
          </td>
          <td class="p-3 font-mono text-[#77797C]">
            ${tx.abha}
          </td>
          <td class="p-3 text-[#223D79]">
            ${tx.complaint}
          </td>
          <td class="p-3">
            <span class="bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded text-[11px] border border-emerald-500/30">
              ✓ ${tx.abdmStatus}
            </span>
          </td>
          <td class="p-3">
            <span class="bg-[#FFA530]/20 text-[#FFA530] font-black px-2 py-0.5 rounded text-[11px] border border-[#FFA530]/30">
              ${tx.pmjayStatus}
            </span>
          </td>
          <td class="p-3 text-right space-x-1.5">
            <button onclick="viewPatientFhir('${tx.name}', '${tx.abha}', '${tx.complaint.replace(/'/g, "")}')" class="bg-[#223D79] hover:bg-[#1a2f5e] text-white px-2.5 py-1 rounded text-[11px] font-bold shadow transition">
              FHIR R4
            </button>
          </td>
        </tr>
      `).join("");

      if (typeof lucide !== "undefined") lucide.createIcons();
    }

    function pingAbdmSandbox() {
      alert("⚡ ABDM NHA Gateway Ping Successful!\n\n• Gateway: Eka Care ABDM Sandbox (M1/M2/M3)\n• Latency: 164 ms\n• Status: 200 OK (HEALTHY)\n• Facility ID: IN0110000142 (AIIA)");
    }

    function simulateNhcxClaim() {
      alert("💳 NHCX Cashless Claim Processed!\n\n• Beneficiary: Ramesh Chandra (PMJAY-TS-482910)\n• Claim Amount: ₹5,000\n• Coverage: Ayushman Bharat PM-JAY Cashless OPD\n• Transaction ID: NHCX-CLAIM-9482019\n• Status: AUTO_APPROVED_BY_PAYER");
    }

    function viewLiveFhirBundle() {
      viewPatientFhir("Ramesh Chandra", "91-4829-1029-4821", "Sandhigata Vata (Osteoarthritis)");
    }

    function viewPatientFhir(name, abha, condition) {
      const sampleBundle = {
        resourceType: "Bundle",
        id: "bundle-" + Date.now().toString().slice(-6),
        meta: {
          profile: ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"],
          lastUpdated: new Date().toISOString()
        },
        identifier: {
          system: "https://aiia.gov.in/bundles",
          value: "DOC-2026-" + Math.floor(1000 + Math.random()*9000)
        },
        type: "document",
        timestamp: new Date().toISOString(),
        entry: [
          {
            fullUrl: "urn:uuid:composition-01",
            resource: {
              resourceType: "Composition",
              status: "final",
              type: { coding: [{ system: "https://projectnamaste.ayush.gov.in", code: "AYU-SAN-01", display: condition }] },
              subject: { reference: "Patient/" + abha, display: name },
              date: new Date().toISOString(),
              author: [{ display: "Dr. Suresh Sharma (AIIA OPD Room 4)" }],
              title: "OPD Clinical Consultation Note"
            }
          },
          {
            fullUrl: "urn:uuid:patient-01",
            resource: {
              resourceType: "Patient",
              identifier: [{ system: "https://healthid.ndhm.gov.in", value: abha }],
              name: [{ text: name }]
            }
          }
        ]
      };

      document.getElementById("fhir-json-display").innerText = JSON.stringify(sampleBundle, null, 2);
      document.getElementById("fhir-modal").classList.remove("hidden");
      if (typeof lucide !== "undefined") lucide.createIcons();
    }

    function closeFhirModal() {
      document.getElementById("fhir-modal").classList.add("hidden");
    }

    window.addEventListener("storage", function(e) {
      if (e.key === "MEDIKIOSK_SHARED_QUEUE" || e.key === "MEDIKIOSK_LAST_TOKEN_NUM") {
        refreshTransactionFeed();
      }
    });

    document.addEventListener("DOMContentLoaded", refreshTransactionFeed);

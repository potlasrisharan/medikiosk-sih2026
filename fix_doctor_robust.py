import re

with open('doctor.html', 'r') as f:
    content = f.read()

# Replace initDoctorQueue with robust dual-sync (LocalStorage + Supabase + Fallback mapping)
robust_init = """async function initDoctorQueue() {
      // 1. Instant local cache merge
      try {
        const localQ = JSON.parse(localStorage.getItem("MEDIKIOSK_SHARED_QUEUE") || "[]");
        localQ.forEach(item => {
          if (item && (item.id || item.encId)) {
            const key = item.id || item.encId;
            CLINICAL_PROFILES[key] = {
              ...item,
              id: key,
              tokenNumber: item.tokenNumber || item.token || "#001"
            };
          }
        });
      } catch (e) {}

      // 2. Supabase Cloud Sync
      try {
        if (window.supabase) {
          const { data, error } = await window.supabase
            .from('encounters')
            .select('*')
            .order('created_at', { ascending: false });
          
          if (!error && data) {
            data.forEach(row => {
              if (row.ui_data && (row.ui_data.id || row.ui_data.encId)) {
                const key = row.ui_data.id || row.ui_data.encId;
                CLINICAL_PROFILES[key] = {
                  ...row.ui_data,
                  id: key,
                  tokenNumber: row.ui_data.tokenNumber || row.token_number || "#001"
                };
              } else if (row.id) {
                CLINICAL_PROFILES[row.id] = {
                  id: row.id,
                  tokenNumber: row.token_number || "#001",
                  patientName: row.patient_name || "Patient",
                  age: row.age || 45,
                  gender: row.gender === 'FEMALE' ? 'Female' : 'Male',
                  hasPmjay: row.pmjay_eligible || false,
                  isEmergency: row.triage_priority === 'EMERGENCY_RED',
                  subjective: row.chief_complaint || "Routine consultation",
                  englishTranslation: row.chief_complaint || "Routine consultation",
                  nativeLang: row.language || "English",
                  avatar: (row.patient_name || "PT").split(" ").map(n => n[0]).join("").slice(0,2).toUpperCase(),
                  assessment: "1. Clinical OPD Evaluation",
                  planSummary: "Physician Evaluation & Personalized Pharmacological Prescribing",
                  aiSuggestions: [],
                  activePrescription: []
                };
              }
            });
          }
        }
      } catch (e) {
        console.error("Supabase queue fetch error:", e);
      }

      // 3. Render Queue List sorted by Priority (Emergency STAT first)
      const allEncIds = Object.keys(CLINICAL_PROFILES);
      allEncIds.sort((a, b) => {
        const pA = CLINICAL_PROFILES[a];
        const pB = CLINICAL_PROFILES[b];
        if (pA.isEmergency && !pB.isEmergency) return -1;
        if (!pA.isEmergency && pB.isEmergency) return 1;
        return 0;
      });

      const queueListEl = document.getElementById("queue-list");
      const countEl = document.getElementById("queue-count");
      if (countEl) countEl.innerText = allEncIds.length.toString();

      if (queueListEl) {
        queueListEl.innerHTML = allEncIds.map((encId, idx) => {
          const p = CLINICAL_PROFILES[encId] || {};
          const isSelected = (encId === currentSelectedEncId);
          const borderClass = p.isEmergency 
            ? (isSelected ? "border-2 border-rose-500 bg-rose-50" : "border border-rose-500/60 bg-white")
            : (isSelected ? "border-2 border-blue-500/50 bg-blue-50" : "border-[#D9CDBA]/60 bg-white border shadow-sm/60");

          const tokenDisplay = p.tokenNumber || p.token || `#${encId.slice(-3)}`;
          const patName = p.patientName || "Walk-In Patient";
          const patAge = p.age || 45;
          const patGen = p.gender === "Female" ? "F" : "M";

          return `
            <div id="queue-item-${encId}" onclick="selectEncounter('${encId}')" class="p-4 rounded-xl border ${borderClass} hover:border-blue-400/50 transition cursor-pointer space-y-2 group">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black px-2.5 py-0.5 rounded bg-[#D9CDBA]/30 text-[#223D79] flex items-center gap-1.5">
                  ${p.isEmergency ? '<span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>' : ''}
                  ${tokenDisplay}
                </span>
                <span class="text-xs ${p.isEmergency ? 'text-rose-600 bg-rose-100 px-2 py-0.5 rounded' : (p.hasPmjay ? 'text-emerald-700' : 'text-[#77797C]')} font-bold">
                  ${p.isEmergency ? 'STAT EMERGENCY' : (p.hasPmjay ? 'PM-JAY Active' : 'General')}
                </span>
              </div>
              <div>
                <h4 class="font-bold text-sm text-[#223D79]">${patName} (${patAge}${patGen})</h4>
                <p class="text-xs text-[#77797C] line-clamp-1 mt-0.5">${p.englishTranslation || p.subjective || 'Clinical evaluation requested'}</p>
              </div>
              <div class="flex items-center justify-between text-[11px] text-[#77797C] pt-1 border-t border-[#D9CDBA]/60">
                <span>ALLOPATHIC</span>
                <span>Just now</span>
              </div>
            </div>
          `;
        }).join("");
      }

      // Auto select first encounter if available and nothing selected
      if (!currentSelectedEncId && allEncIds.length > 0) {
        selectEncounter(allEncIds[0]);
      }
    }"""

# Replace initDoctorQueue block
content = re.sub(r'async function initDoctorQueue\(\) \{.*?\n\s*if \(\!currentSelectedEncId && allEncIds\.length > 0\) \{\n\s*selectEncounter\(allEncIds\[0\]\);\n\s*\}\n\s*\}', robust_init, content, flags=re.DOTALL)

# Re-enable storage event listener for instant tab switching
if 'window.addEventListener("storage"' not in content:
    content += """\n<script>
    window.addEventListener("storage", function(e) {
      if (e.key === "MEDIKIOSK_SHARED_QUEUE" || e.key === "MEDIKIOSK_LAST_TOKEN_NUM") {
        initDoctorQueue();
      }
    });
    </script>"""

with open('doctor.html', 'w') as f:
    f.write(content)
print("doctor.html fully robustified")

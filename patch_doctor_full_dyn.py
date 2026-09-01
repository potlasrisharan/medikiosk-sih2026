import re

with open('doctor.html', 'r') as f:
    content = f.read()

# 1. Replace static lab badges with dynamic container
static_labs = """            <div class="space-y-2 pt-1">
              <div class="flex justify-between items-center bg-rose-50 border border-rose-200 px-3 py-1.5 rounded-xl text-xs">
                <span class="font-bold text-rose-900">Serum Uric Acid</span>
                <span class="font-black text-rose-700">7.8 mg/dL <span class="text-[10px] bg-rose-600 text-white px-1.5 py-0.5 rounded font-black">HIGH</span></span>
              </div>
              <div class="flex justify-between items-center bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-xl text-xs">
                <span class="text-slate-600 font-semibold">HbA1c</span>
                <span class="font-bold text-slate-900">6.1 %</span>
              </div>
            </div>"""

dynamic_labs = """            <div id="soap-o-labs" class="space-y-2 pt-1">
              <!-- Dynamically populated per patient in selectEncounter() -->
            </div>"""

content = content.replace(static_labs, dynamic_labs)

# 2. Update selectEncounter to populate #soap-o-labs dynamically
old_soap_o = """      // 4. Update O: Objective & Labs
      const soapOEl = document.getElementById("soap-o");
      if (soapOEl) soapOEl.innerText = data.objective;"""

new_soap_o = """      // 4. Update O: Objective & Labs
      const soapOEl = document.getElementById("soap-o");
      if (soapOEl) soapOEl.innerText = data.objective || "Clinical Vitals: [Pending In-Person Chamber Measurement]";

      const labsContainer = document.getElementById("soap-o-labs");
      if (labsContainer) {
        if (encId === "enc-0042" || (data.patientName && data.patientName.includes("Ramesh"))) {
          labsContainer.innerHTML = `
            <div class="flex justify-between items-center bg-rose-50 border border-rose-200 px-3 py-1.5 rounded-xl text-xs">
              <span class="font-bold text-rose-900">Serum Uric Acid</span>
              <span class="font-black text-rose-700">7.8 mg/dL <span class="text-[10px] bg-rose-600 text-white px-1.5 py-0.5 rounded font-black">HIGH</span></span>
            </div>
            <div class="flex justify-between items-center bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-xl text-xs">
              <span class="text-slate-600 font-semibold">HbA1c</span>
              <span class="font-bold text-slate-900">6.1 %</span>
            </div>
          `;
        } else if (encId === "enc-0043" || (data.patientName && data.patientName.includes("Priya"))) {
          labsContainer.innerHTML = `
            <div class="flex justify-between items-center bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-xl text-xs">
              <span class="font-bold text-amber-900">Upper GI Endoscopy</span>
              <span class="font-bold text-amber-700">Antral Gastritis</span>
            </div>
            <div class="flex justify-between items-center bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-xl text-xs">
              <span class="text-emerald-700 font-semibold">H. Pylori Stool Ag</span>
              <span class="font-bold text-emerald-800">Negative (Normal)</span>
            </div>
          `;
        } else if (data.isEmergency || (data.patientName && data.patientName.includes("Mohan"))) {
          labsContainer.innerHTML = `
            <div class="flex justify-between items-center bg-rose-50 border border-rose-300 px-3 py-1.5 rounded-xl text-xs animate-pulse">
              <span class="font-bold text-rose-900">STAT Cardiac Troponin-I</span>
              <span class="font-black text-rose-700">1.84 ng/mL <span class="text-[10px] bg-rose-600 text-white px-1.5 py-0.5 rounded font-black">CRITICAL</span></span>
            </div>
            <div class="flex justify-between items-center bg-rose-50 border border-rose-200 px-3 py-1.5 rounded-xl text-xs">
              <span class="text-rose-800 font-bold">12-Lead ECG</span>
              <span class="font-black text-rose-700">ST-Elevation V1-V4 (STEMI)</span>
            </div>
          `;
        } else {
          labsContainer.innerHTML = `
            <div class="flex justify-between items-center bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-xl text-xs">
              <span class="text-slate-600 font-semibold">Digitized Document Status</span>
              <span class="font-bold text-emerald-600">✓ Intake Complete</span>
            </div>
          `;
        }
      }"""

content = content.replace(old_soap_o, new_soap_o)

with open('doctor.html', 'w') as f:
    f.write(content)
print("Dynamic lab badges patched in doctor.html!")

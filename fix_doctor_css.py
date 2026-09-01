import re
with open('doctor.html', 'r') as f:
    content = f.read()

# Replace the innerHTML template in initDoctorQueue
old_template = r'queueListEl\.innerHTML = allEncIds\.map\(encId => \{.*?return `.*?`;\n\s*\}\)\.join\(""\);'

new_template = """queueListEl.innerHTML = allEncIds.map((encId, idx) => {
          const p = CLINICAL_PROFILES[encId];
          const isSelected = (encId === currentSelectedEncId);
          const borderClass = p.isEmergency 
            ? (isSelected ? "border-2 border-rose-500 bg-rose-50" : "border border-rose-500/60 bg-white")
            : (isSelected ? "border-2 border-blue-500/50 bg-blue-50" : "border-[#D9CDBA]/60 bg-white border shadow-sm/60");

          return `
            <div id="queue-item-${encId}" onclick="selectEncounter('${encId}')" class="p-4 rounded-xl border ${borderClass} hover:border-blue-400/50 transition cursor-pointer space-y-2 group">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black px-2.5 py-0.5 rounded bg-[#D9CDBA]/30 text-[#223D79] flex items-center gap-1.5">
                  ${p.isEmergency ? '<span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>' : ''}
                  ${p.tokenNumber}
                </span>
                <span class="text-xs ${p.isEmergency ? 'text-rose-600 bg-rose-100 px-2 py-0.5 rounded' : (p.hasPmjay ? 'text-emerald-700' : 'text-[#77797C]')} font-bold">
                  ${p.isEmergency ? 'STAT EMERGENCY' : (p.hasPmjay ? 'PM-JAY Active' : 'General')}
                </span>
              </div>
              <div>
                <h4 class="font-bold text-sm text-[#223D79]">${p.patientName} (${p.age}${p.gender === 'Male' ? 'M' : 'F'})</h4>
                <p class="text-xs text-[#77797C] line-clamp-1 mt-0.5">${p.englishTranslation || p.subjective || ''}</p>
              </div>
              <div class="flex items-center justify-between text-[11px] text-[#77797C] pt-1 border-t border-[#D9CDBA]/60">
                <span>ALLOPATHIC</span>
                <span>Just now</span>
              </div>
            </div>
          `;
        }).join("");"""

content = re.sub(old_template, new_template, content, flags=re.DOTALL)

# Also fix the selectEncounter class changing logic which changes the colors dynamically
select_pattern = r'allEncIds\.forEach\(k => \{\n\s*const item = document\.getElementById\(`queue-item-\$\{k\}`\);\n\s*if \(\!item\) return;\n\s*const p = CLINICAL_PROFILES\[k\];\n\s*if \(k === encId\) \{\n\s*item\.className = "p-3\.5 rounded-xl border-2 " \+ \(p && p\.isEmergency \? "border-rose-500 bg-rose-100" : "border-\[\#FFA530\] bg-\[\#223D79\] text-\[\#223D79\]"\) \+ " cursor-pointer transition shadow-md group";\n\s*\} else \{\n\s*item\.className = "p-3\.5 rounded-xl border " \+ \(p && p\.isEmergency \? "border-rose-500/50 bg-rose-50" : "border-\[\#D9CDBA\]/30 bg-white border border-\[\#D9CDBA\]/80 shadow-sm"\) \+ " hover:bg-\[\#223D79\] text-white/60 cursor-pointer transition shadow-sm group";\n\s*\}\n\s*\}\);'

select_replace = """allEncIds.forEach(k => {
        const item = document.getElementById(`queue-item-${k}`);
        if (!item) return;
        const p = CLINICAL_PROFILES[k];
        if (k === encId) {
          item.className = "p-4 rounded-xl border-2 " + (p && p.isEmergency ? "border-rose-500 bg-rose-50" : "border-blue-500/50 bg-blue-50") + " cursor-pointer transition space-y-2 group";
        } else {
          item.className = "p-4 rounded-xl border " + (p && p.isEmergency ? "border-rose-500/60 bg-white" : "border-[#D9CDBA]/60 bg-white shadow-sm/60") + " hover:border-blue-400/50 cursor-pointer transition space-y-2 group";
        }
      });"""

content = re.sub(select_pattern, select_replace, content, flags=re.DOTALL)

with open('doctor.html', 'w') as f:
    f.write(content)
print("doctor.html CSS restored and enhanced")

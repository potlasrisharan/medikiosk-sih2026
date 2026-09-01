with open('index.html', 'r') as f:
    content = f.read()

# 1. Update triggerImmediateEmergency queue push
emerg_push_old = """      // 3. Push to queue
      await window.supabase.from('encounters').insert([{
         id: newEncounter.id,
         token_number: newEncounter.tokenNumber,
         patient_id: newEncounter.abhaId || "pat-unknown",
         patient_name: newEncounter.patientName,
         age: newEncounter.age,
         gender: newEncounter.gender.toUpperCase(),
         chief_complaint: newEncounter.englishTranslation || newEncounter.subjective,
         triage_priority: newEncounter.isEmergency ? 'EMERGENCY_RED' : 'ROUTINE',
         pmjay_eligible: newEncounter.hasPmjay || false,
         system_type: 'ALLOPATHIC',
         status: newEncounter.isEmergency ? 'EMERGENCY_TRIAGE' : 'WAITING',
         language: newEncounter.nativeLang,
         ui_data: newEncounter
      }]);"""

emerg_push_new = """      // 3. Push to queue (Dual Storage: LocalStorage + Supabase Cloud)
      try {
        let q = JSON.parse(localStorage.getItem("MEDIKIOSK_SHARED_QUEUE") || "[]");
        q.unshift(newEncounter);
        localStorage.setItem("MEDIKIOSK_SHARED_QUEUE", JSON.stringify(q));
      } catch (e) {}

      try {
        if (window.supabase) {
          await window.supabase.from('encounters').insert([{
             id: newEncounter.id,
             token_number: newEncounter.tokenNumber,
             patient_id: "pat-unknown",
             patient_name: newEncounter.patientName,
             age: newEncounter.age,
             gender: newEncounter.gender.toUpperCase(),
             chief_complaint: newEncounter.englishTranslation || newEncounter.subjective,
             triage_priority: 'EMERGENCY_RED',
             pmjay_eligible: false,
             system_type: 'ALLOPATHIC',
             status: 'EMERGENCY_TRIAGE',
             language: newEncounter.nativeLang,
             ui_data: newEncounter
          }]);
        }
      } catch (err) {
        console.warn("Supabase background sync notice:", err);
      }"""

content = content.replace(emerg_push_old, emerg_push_new)

# 2. Update generateDynamicTokenAndRegister queue push
routine_push_old = """      await window.supabase.from('encounters').insert([{
         id: newEncounter.id,
         token_number: newEncounter.tokenNumber,
         patient_id: newEncounter.abhaId || "pat-unknown",
         patient_name: newEncounter.patientName,
         age: newEncounter.age,
         gender: (newEncounter.gender || "Unknown").toUpperCase(),
         chief_complaint: newEncounter.englishTranslation || newEncounter.subjective,
         triage_priority: newEncounter.isEmergency ? 'EMERGENCY_RED' : 'ROUTINE',
         pmjay_eligible: newEncounter.hasPmjay || false,
         system_type: 'ALLOPATHIC',
         status: newEncounter.isEmergency ? 'EMERGENCY_TRIAGE' : 'WAITING',
         language: newEncounter.nativeLang,
         ui_data: newEncounter
      }]);"""

routine_push_new = """      // Push to queue (Dual Storage: LocalStorage + Supabase Cloud)
      try {
        let q = JSON.parse(localStorage.getItem("MEDIKIOSK_SHARED_QUEUE") || "[]");
        q.unshift(newEncounter);
        localStorage.setItem("MEDIKIOSK_SHARED_QUEUE", JSON.stringify(q));
      } catch (e) {}

      try {
        if (window.supabase) {
          await window.supabase.from('encounters').insert([{
             id: newEncounter.id,
             token_number: newEncounter.tokenNumber,
             patient_id: "pat-unknown",
             patient_name: newEncounter.patientName,
             age: newEncounter.age,
             gender: (newEncounter.gender || "Unknown").toUpperCase(),
             chief_complaint: newEncounter.englishTranslation || newEncounter.subjective,
             triage_priority: newEncounter.isEmergency ? 'EMERGENCY_RED' : 'ROUTINE',
             pmjay_eligible: newEncounter.hasPmjay || false,
             system_type: 'ALLOPATHIC',
             status: newEncounter.isEmergency ? 'EMERGENCY_TRIAGE' : 'WAITING',
             language: newEncounter.nativeLang,
             ui_data: newEncounter
          }]);
        }
      } catch (err) {
        console.warn("Supabase background sync notice:", err);
      }"""

content = content.replace(routine_push_old, routine_push_new)

with open('index.html', 'w') as f:
    f.write(content)
print("index.html dual queue storage patched")

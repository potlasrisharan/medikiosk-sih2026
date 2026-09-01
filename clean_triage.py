import re
with open('triage.html', 'r') as f:
    content = f.read()

# Replace getSharedQueue to just return [] since renderTriageQueue bypasses it anyway now
content = re.sub(r'function getSharedQueue\(\) \{.*?\n\s*\}\n\s*\}', 'function getSharedQueue() { return []; }', content, flags=re.DOTALL)

# In triggerSimulatedEmergency, we replace the queue.unshift logic
sim_pattern = r'queue\.unshift\(newEmerg\);\n\s*localStorage\.setItem\("MEDIKIOSK_SHARED_QUEUE", JSON\.stringify\(queue\)\);'
sim_replace = """await window.supabase.from('encounters').insert([{
         id: newEmerg.encId,
         token_number: newEmerg.tokenNumber || newEmerg.token,
         patient_id: "pat-unknown",
         patient_name: newEmerg.patientName,
         age: newEmerg.age,
         gender: newEmerg.gender,
         chief_complaint: newEmerg.englishTranslation || newEmerg.subjective,
         triage_priority: 'EMERGENCY_RED',
         pmjay_eligible: newEmerg.hasPmjay || false,
         system_type: 'ALLOPATHIC',
         status: 'EMERGENCY_TRIAGE',
         language: newEmerg.nativeLang,
         ui_data: newEmerg
      }]);"""
content = re.sub(sim_pattern, sim_replace, content)

with open('triage.html', 'w') as f:
    f.write(content)
print("triage.html strictly cleaned")

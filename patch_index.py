import re

with open('index.html', 'r') as f:
    content = f.read()

# Pattern for emergency zero-click
emergency_pattern = r'let sharedQueue = \[\];\n\s*try \{\n\s*sharedQueue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*\} catch \(e\) \{\}\n\s*sharedQueue\.unshift\(newEncounter\);\n\s*localStorage\.setItem\("MEDIKIOSK_SHARED_QUEUE", JSON\.stringify\(sharedQueue\)\);'

emergency_replace = """
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
      }]);
"""
content = re.sub(emergency_pattern, emergency_replace.strip(), content)

# Pattern for regular encounter
regular_pattern = r'// Push to shared localStorage queue for instant cross-tab sync with Doctor Portal\n\s*let sharedQueue = \[\];\n\s*try \{\n\s*sharedQueue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*\} catch \(e\) \{\}\n\n\s*// Add to front of queue\n\s*sharedQueue\.unshift\(newEncounter\);\n\s*localStorage\.setItem\("MEDIKIOSK_SHARED_QUEUE", JSON\.stringify\(sharedQueue\)\);'

regular_replace = """
      await window.supabase.from('encounters').insert([{
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
      }]);
"""
content = re.sub(regular_pattern, regular_replace.strip(), content)

with open('index.html', 'w') as f:
    f.write(content)

print("index.html updated")

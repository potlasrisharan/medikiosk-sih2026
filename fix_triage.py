import re
with open('triage.html', 'r') as f:
    content = f.read()

# Replace getSharedQueue to not do anything, or we just replace renderTriageQueue
# We need to make renderTriageQueue async and fetch from Supabase.
render_pattern = r'function renderTriageQueue\(\) \{\n\s*const queue = getSharedQueue\(\);\n\s*const container = document\.getElementById\("triage-cards-container"\);\n\s*if \(\!container\) return;\n\n\s*// Extract all emergency items\n\s*let emergencyItems = queue\.filter\(item => item\.isEmergency === true \|\| \(item\.tokenNumber && item\.tokenNumber\.includes\("E-"\)\) \|\| \(item\.token && item\.token\.includes\("E-"\)\)\);'

render_replace = """async function renderTriageQueue() {
      const container = document.getElementById("triage-cards-container");
      if (!container) return;

      let emergencyItems = [];
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .eq('triage_priority', 'EMERGENCY_RED')
          .order('created_at', { ascending: false });
          
        if (!error && data) {
           emergencyItems = data.map(r => r.ui_data).filter(x => x);
        }
      } catch (e) {}"""

content = re.sub(render_pattern, render_replace, content)

# Now fix the Simulated Emergency button to insert to Supabase instead of localStorage
sim_pattern = r'let queue = getSharedQueue\(\);\n\s*queue\.unshift\(newEmerg\);\n\s*localStorage\.setItem\("MEDIKIOSK_SHARED_QUEUE", JSON\.stringify\(queue\)\);\n\s*renderTriageQueue\(\);'
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
      }]);
      renderTriageQueue();"""

content = re.sub(sim_pattern, sim_replace, content)
content = content.replace('function triggerSimulatedEmergency() {', 'async function triggerSimulatedEmergency() {')

with open('triage.html', 'w') as f:
    f.write(content)
print("triage.html patched for supabase")

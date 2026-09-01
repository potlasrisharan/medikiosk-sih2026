import re
with open('triage.html', 'r') as f:
    content = f.read()

getq_start = content.find('function getSharedQueue() {')
if getq_start != -1:
    getq_end = content.find('}', content.find('return', getq_start)) + 1
    
    # We will just change renderTriageQueue
    render_start = content.find('function renderTriageQueue() {')
    render_end = content.find('}', content.find('emergenciesContainer.innerHTML =', render_start)) + 1
    
    # Actually, it's easier to replace the specific localStorage bits
    
    # For writing to queue:
    write_pattern = r'let queue = getSharedQueue\(\);\n\s*queue\.unshift\(newEmerg\);\n\s*localStorage\.setItem\("MEDIKIOSK_SHARED_QUEUE", JSON\.stringify\(queue\)\);'
    write_replace = """
      await window.supabase.from('encounters').insert([{
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
"""
    content = re.sub(write_pattern, write_replace.strip(), content)

    # For reading queue in renderTriageQueue:
    render_pattern = r'function renderTriageQueue\(\) \{\n\s*const queue = getSharedQueue\(\);\n\s*let emergencyItems = queue\.filter\(item => item\.isEmergency === true \|\| \(item\.tokenNumber && item\.tokenNumber\.includes\("E-"\)\) \|\| \(item\.token && item\.token\.includes\("E-"\)\)\);'
    
    render_replace = """async function renderTriageQueue() {
      const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .eq('triage_priority', 'EMERGENCY_RED')
          .order('created_at', { ascending: false });
      
      let emergencyItems = [];
      if (!error && data) {
         emergencyItems = data.map(r => r.ui_data).filter(x => x);
      }"""
    content = re.sub(render_pattern, render_replace, content)
    
    with open('triage.html', 'w') as f:
        f.write(content)
    print("triage patched")

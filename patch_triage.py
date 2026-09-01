import re

with open('triage.html', 'r') as f:
    content = f.read()

queue_pattern = r'function fetchQueue\(\) \{\n\s*try \{\n\s*let queue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*// Only show emergency\n\s*const emergencies = queue\.filter\(q => q\.isEmergency\);\n\s*emergencies\.forEach\(item => \{\n\s*TRIAGE_PROFILES\[item\.encId\] = item;\n\s*\}\);\n\s*renderQueue\(\);\n\s*if \(!currentSelectedEncId && emergencies\.length > 0\) \{\n\s*selectEncounter\(emergencies\[0\]\.encId\);\n\s*\}\n\s*\} catch \(e\) \{\n\s*console\.error\("Error fetching queue", e\);\n\s*\}\n\s*\}'

queue_replace = """
    async function fetchQueue() {
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .eq('triage_priority', 'EMERGENCY_RED')
          .order('created_at', { ascending: false });
        if (error) throw error;
        
        let hasNew = false;
        data.forEach(row => {
          if (row.ui_data && row.ui_data.encId) {
             TRIAGE_PROFILES[row.ui_data.encId] = row.ui_data;
             hasNew = true;
          }
        });
        renderQueue();
        if (!currentSelectedEncId && data.length > 0) {
          selectEncounter(data[0].ui_data.encId);
        }
      } catch (e) {
        console.error("Error fetching queue", e);
      }
    }
"""
content = re.sub(queue_pattern, queue_replace.strip(), content)

if 'setInterval(fetchQueue' not in content:
    content = content.replace("fetchQueue();", "fetchQueue();\n    setInterval(fetchQueue, 3000);")

with open('triage.html', 'w') as f:
    f.write(content)

print("triage.html updated")

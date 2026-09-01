with open('doctor_old.html', 'r') as f:
    content = f.read()

# I will recreate doctor.html starting from doctor_old.html, so I know I didn't break any tailwind classes
# 1. Add supabase scripts
if 'supabase-js' not in content:
    content = content.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n  <script src="supabase-client.js"></script>\n</head>')

# 2. Replace the fetchQueue block. In old it had:
import re
# Remove fetchQueue and renderDynamicQueue and fetchQueue_old
content = re.sub(r'async function fetchQueue\(\) \{.*?\n\s*\}\n\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'function renderDynamicQueue\(queue\) \{.*?\n\s*\}\n\s*\`\)\.join\(""\);\n\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'async function fetchQueue_old\(\) \{.*?\n\s*\}\n\s*\}', '', content, flags=re.DOTALL)

# 3. Modify initDoctorQueue to use Supabase
init_pattern = r'function initDoctorQueue\(\) \{\n\s*let customQueue = \[\];\n\s*try \{\n\s*customQueue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*\} catch \(e\) \{\}\n\n\s*// Merge custom encounters into CLINICAL_PROFILES\n\s*customQueue\.forEach\(item => \{\n\s*if \(item && item\.id\) \{\n\s*CLINICAL_PROFILES\[item\.id\] = item;\n\s*\}\n\s*\}\);'

init_replace = """async function initDoctorQueue() {
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .order('created_at', { ascending: false });
        if (error) throw error;
        
        data.forEach(row => {
          if (row.ui_data && row.ui_data.id) {
             CLINICAL_PROFILES[row.ui_data.id] = row.ui_data;
          }
        });
      } catch (e) {
        console.error("Error fetching queue", e);
      }"""
content = re.sub(init_pattern, init_replace, content)

# 4. Add setInterval for auto-refresh
if 'setInterval(initDoctorQueue' not in content:
    content = content.replace('document.addEventListener("DOMContentLoaded", initDoctorQueue);', 'document.addEventListener("DOMContentLoaded", () => { initDoctorQueue(); setInterval(initDoctorQueue, 3000); });')

with open('doctor.html', 'w') as f:
    f.write(content)
print("Rewrote doctor.html from old version")

import re

with open('doctor.html', 'r') as f:
    content = f.read()

queue_pattern = r'function fetchQueue\(\) \{\n\s*try \{\n\s*let queue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*// Sync to internal CLINICAL_PROFILES\n\s*queue\.forEach\(item => \{\n\s*CLINICAL_PROFILES\[item\.encId\] = item;\n\s*\}\);\n\s*renderQueue\(\);\n\s*\} catch \(e\) \{\n\s*console\.error\("Error fetching queue", e\);\n\s*\}\n\s*\}'

queue_replace = """
    async function fetchQueue() {
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .order('created_at', { ascending: false });
        if (error) throw error;
        
        data.forEach(row => {
          if (row.ui_data && row.ui_data.encId) {
             CLINICAL_PROFILES[row.ui_data.encId] = row.ui_data;
          }
        });
        renderQueue();
      } catch (e) {
        console.error("Error fetching queue", e);
      }
    }
"""
content = re.sub(queue_pattern, queue_replace.strip(), content)

# Remove localStorage storage event listener since we need Supabase realtime or polling
# Actually polling is easier: add setInterval(fetchQueue, 3000) inside DOMContentLoaded or similar.
# There's already: window.addEventListener('storage', fetchQueue);
# Let's add a setInterval as well.
if 'setInterval(fetchQueue' not in content:
    content = content.replace("fetchQueue();", "fetchQueue();\n    setInterval(fetchQueue, 3000);")

with open('doctor.html', 'w') as f:
    f.write(content)

print("doctor.html updated")

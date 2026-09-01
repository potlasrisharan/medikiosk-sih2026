with open('doctor.html', 'r') as f:
    content = f.read()

content = content.replace('async async function fetchQueue() {', 'async function fetchQueue() {')

# The extra '}' is because I replaced something poorly in patch_doctor2.py
# Let's clean it up using regex.
import re
pattern = r'async function fetchQueue\(\) \{\n.*?\}\n\s*\}\n\n\s*async function selectEncounter'
replace = r'async function fetchQueue() {\n      try {\n        const { data, error } = await window.supabase\n          .from(\'encounters\')\n          .select(\'*\')\n          .order(\'created_at\', { ascending: false });\n        if (error) throw error;\n        \n        data.forEach(row => {\n          if (row.ui_data && row.ui_data.encId) {\n             CLINICAL_PROFILES[row.ui_data.encId] = row.ui_data;\n          }\n        });\n        renderQueue();\n      } catch (e) {\n        console.error("Error fetching queue", e);\n      }\n    }\n\n    async function selectEncounter'

# wait, regex with multiline is tricky. Let's just fix the exact string.
content = content.replace('    }\n    }\n\n    async function selectEncounter', '    }\n\n    async function selectEncounter')

with open('doctor.html', 'w') as f:
    f.write(content)
print("Fixed doctor.html syntax error")

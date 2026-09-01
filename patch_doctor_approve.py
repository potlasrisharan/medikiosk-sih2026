import re
with open('doctor.html', 'r') as f:
    content = f.read()

# Pattern for localStorage queue removal in approvePrescription
pattern = r'try \{\n\s*let queue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*let updated = queue\.filter\(q => q\.encId !== currentSelectedEncId \|\| q\.id !== currentSelectedEncId\);\n\s*localStorage\.setItem\("MEDIKIOSK_SHARED_QUEUE", JSON\.stringify\(updated\)\);\n\s*\} catch \(e\) \{\}'

replace = """try {
          await window.supabase.from('encounters').update({ status: 'COMPLETED' }).eq('id', currentSelectedEncId);
        } catch (e) {
          console.error("Supabase update error:", e);
        }"""

content = re.sub(pattern, replace, content, flags=re.DOTALL)

with open('doctor.html', 'w') as f:
    f.write(content)
print("doctor.html approve patched")

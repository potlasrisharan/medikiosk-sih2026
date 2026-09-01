import re
with open('index.html', 'r') as f:
    content = f.read()

pattern = r'const btn = document\.getElementById\("btn-confirm-token"\);\n\s*const originalText = btn\.innerText;\n\s*btn\.innerText = "⚡ Sarvam-105B Evaluating Triage & Pharmacology\.\.\.";\n\s*btn\.disabled = true;'

replace = """const btn = document.getElementById("btn-confirm-token");
      const skipBtn = document.getElementById("btn-skip-rx");
      const originalText = btn ? btn.innerText : "";
      const originalSkipText = skipBtn ? skipBtn.innerText : "";
      if (btn) { btn.innerText = "⚡ Sarvam-105B Evaluating Triage..."; btn.disabled = true; }
      if (skipBtn) { skipBtn.innerText = "⚡ Evaluatng Triage..."; skipBtn.disabled = true; }"""

content = re.sub(pattern, replace, content)

restore_pattern = r'// Reset button\n\s*btn\.innerText = originalText;\n\s*btn\.disabled = false;'
restore_replace = """// Reset button
      if (btn) { btn.innerText = originalText; btn.disabled = false; }
      if (skipBtn) { skipBtn.innerText = originalSkipText; skipBtn.disabled = false; }"""

content = re.sub(restore_pattern, restore_replace, content)

with open('index.html', 'w') as f:
    f.write(content)
print("Loaders fixed")

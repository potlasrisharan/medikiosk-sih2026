import re
with open('index.html', 'r') as f:
    content = f.read()

content = content.replace('source_language: currentLang,', 'source_language: currentLanguage,')

with open('index.html', 'w') as f:
    f.write(content)
print("Language typo fixed")

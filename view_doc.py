import re
with open('doctor.html', 'r') as f:
    content = f.read()

matches = re.finditer(r'function (\w+)\(', content)
print("Functions in doctor.html:")
for m in matches:
    print(m.group(1))

with open('ayush.html', 'r') as f:
    content = f.read()

if 'setInterval(loadAyushQueue' not in content:
    content = content.replace('document.addEventListener("DOMContentLoaded", loadAyushQueue);', 'document.addEventListener("DOMContentLoaded", () => { loadAyushQueue(); setInterval(loadAyushQueue, 3000); });')

with open('ayush.html', 'w') as f:
    f.write(content)

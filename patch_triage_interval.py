with open('triage.html', 'r') as f:
    content = f.read()

if 'setInterval(renderTriageQueue' not in content:
    content = content.replace('document.addEventListener("DOMContentLoaded", renderTriageQueue);', 'document.addEventListener("DOMContentLoaded", () => { renderTriageQueue(); setInterval(renderTriageQueue, 3000); });')
    with open('triage.html', 'w') as f:
        f.write(content)

with open('index.html', 'r') as f:
    lines = f.readlines()
start = -1
for i, l in enumerate(lines):
    if 'function stopAllAudio(' in l:
        start = i
        break
end = -1
for i in range(start, len(lines)):
    if 'function playBrowserSynthesis' in lines[i]:
        end = i
        break
print("".join(lines[start:end+15]))

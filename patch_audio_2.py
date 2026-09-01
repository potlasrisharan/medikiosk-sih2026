import re
with open('index.html', 'r') as f:
    content = f.read()

stop_pattern = r'function stopAllAudio\(\) \{\n\s*if \(currentAudioPlayer\) \{'
stop_replace = 'function stopAllAudio() {\n      currentTtsRequestId++;\n      if (currentAudioPlayer) {'

content = re.sub(stop_pattern, stop_replace, content)

with open('index.html', 'w') as f:
    f.write(content)
print("stopAllAudio patched")

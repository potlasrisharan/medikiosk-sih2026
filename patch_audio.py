import re
with open('index.html', 'r') as f:
    content = f.read()

# 1. Add currentTtsRequestId near currentAudioPlayer
var_pattern = r'let currentAudioPlayer = null;'
var_replace = 'let currentAudioPlayer = null;\n    let currentTtsRequestId = 0;'
content = content.replace(var_pattern, var_replace)

# 2. Update stopAllAudio
stop_pattern = r'function stopAllAudio\(\) \{'
stop_replace = 'function stopAllAudio() {\n      currentTtsRequestId++;'
content = content.replace(stop_pattern, stop_replace)

# 3. Update speakAudio fetch logic
fetch_pattern = r'fetch\("/api/v1/ai/tts", \{\n\s*method: "POST",\n\s*headers: \{ "Content-Type": "application/json" \},\n\s*body: JSON\.stringify\(\{ text: cleanText, language_code: currentLanguage \}\)\n\s*\}\)\.then\(res => res\.json\(\)\)\.then\(data => \{\n\s*if \(data && data\.audio_base64 && isVoiceActive\) \{\n\s*currentAudioPlayer = new Audio\("data:audio/wav;base64," \+ data\.audio_base64\);\n\s*currentAudioPlayer\.play\(\)\.catch\(e => console\.log\("Audio play caught:", e\)\);\n\s*\}\n\s*\}\)\.catch\(err => \{\n\s*playBrowserSynthesis\(cleanText\);\n\s*\}\);'

fetch_replace = """const thisRequestId = currentTtsRequestId;
      fetch("/api/v1/ai/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: cleanText, language_code: currentLanguage })
      }).then(res => res.json()).then(data => {
        if (thisRequestId !== currentTtsRequestId) return; // Stale request, audio was stopped/overridden
        if (data && data.audio_base64 && isVoiceActive) {
          currentAudioPlayer = new Audio("data:audio/wav;base64," + data.audio_base64);
          currentAudioPlayer.play().catch(e => console.log("Audio play caught:", e));
        }
      }).catch(err => {
        if (thisRequestId === currentTtsRequestId) {
            playBrowserSynthesis(cleanText);
        }
      });"""
content = re.sub(fetch_pattern, fetch_replace, content)

with open('index.html', 'w') as f:
    f.write(content)

print("index.html audio logic patched")

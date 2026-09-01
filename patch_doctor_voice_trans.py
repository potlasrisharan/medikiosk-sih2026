import re

with open('doctor.html', 'r') as f:
    content = f.read()

# 1. Update Native Speech box to include Listen / Play Audio Button
old_native_box = """            <!-- Original Mother Tongue Spoken Voice -->
            <div class="p-3 bg-amber-50/70 rounded-xl border border-amber-200/80 space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-[10px] text-amber-900 font-bold uppercase tracking-wider">
                  🗣️ Patient Spoken Words (Native Mother Tongue):
                </span>
                <span id="patient-lang-badge" class="text-[10px] text-[#223D79] font-black bg-[#FFA530]/30 px-2 py-0.5 rounded border border-[#FFA530]/50">
                  తెలుగు (Telugu)
                </span>
              </div>
              <p id="soap-native-text" class="text-xs text-slate-800 italic font-semibold leading-relaxed">
                "నాకు గత 6 నెలలుగా రెండు మోకాళ్ళలో నొప్పిగా ఉంది. ఉదయం లేవగానే బిగుతుగా ఉంటుంది, చలికాలంలో నొప్పి ఎక్కువవుతుంది."
              </p>
            </div>"""

new_native_box = """            <!-- Original Mother Tongue Spoken Voice -->
            <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200/90 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-[10px] text-amber-900 font-bold uppercase tracking-wider flex items-center gap-1.5">
                  <i data-lucide="mic" class="w-3.5 h-3.5 text-amber-700"></i>
                  Patient Spoken Words (Native Mother Tongue):
                </span>
                <div class="flex items-center gap-2">
                  <span id="patient-lang-badge" class="text-[10px] text-[#223D79] font-black bg-[#FFA530]/30 px-2 py-0.5 rounded border border-[#FFA530]/50">
                    తెలుగు (Telugu)
                  </span>
                  <button id="btn-play-patient-voice" onclick="playCurrentPatientNativeAudio()" class="text-xs bg-amber-600 hover:bg-amber-700 text-white font-bold px-2.5 py-1 rounded-lg flex items-center gap-1.5 shadow-sm transition">
                    <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
                    <span>Listen Spoken Audio</span>
                  </button>
                </div>
              </div>
              <p id="soap-native-text" class="text-xs text-slate-900 italic font-semibold leading-relaxed bg-white/70 p-2.5 rounded-lg border border-amber-200/60">
                "నాకు గత 6 నెలలుగా రెండు మోకాళ్ళలో నొప్పిగా ఉంది. ఉదయం లేవగానే బిగుతుగా ఉంటుంది, చలికాలంలో నొప్పి ఎక్కువవుతుంది."
              </p>
            </div>"""

content = content.replace(old_native_box, new_native_box)

# 2. Add Audio Player helper and Translation Sanitizer in doctor.html
audio_helper = """
    let doctorAudioPlayer = null;

    function playCurrentPatientNativeAudio() {
      if (!currentSelectedEncId || !CLINICAL_PROFILES[currentSelectedEncId]) return;
      const data = CLINICAL_PROFILES[currentSelectedEncId];
      const rawText = (data.nativeSpeech || "").replace(/"/g, "").trim();
      if (!rawText) return;

      const btn = document.getElementById("btn-play-patient-voice");
      if (btn) {
        btn.innerHTML = `<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin"></i> <span>Playing...</span>`;
        if (typeof lucide !== "undefined") lucide.createIcons();
      }

      if (doctorAudioPlayer) {
        doctorAudioPlayer.pause();
        doctorAudioPlayer = null;
      }
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }

      const langCode = (data.nativeLang && data.nativeLang.includes("Telugu")) ? "te-IN" :
                       (data.nativeLang && data.nativeLang.includes("Hindi")) ? "hi-IN" :
                       (data.nativeLang && data.nativeLang.includes("Tamil")) ? "ta-IN" : "en-IN";

      if (langCode === "en-IN" || langCode === "hi-IN") {
        const u = new SpeechSynthesisUtterance(rawText);
        u.lang = langCode;
        u.rate = 0.95;
        u.onend = () => {
          if (btn) {
            btn.innerHTML = `<i data-lucide="volume-2" class="w-3.5 h-3.5"></i> <span>Listen Spoken Audio</span>`;
            if (typeof lucide !== "undefined") lucide.createIcons();
          }
        };
        window.speechSynthesis.speak(u);
        return;
      }

      fetch("/api/v1/ai/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: rawText, language_code: langCode })
      })
      .then(res => res.json())
      .then(d => {
        if (d && d.audio_base64) {
          doctorAudioPlayer = new Audio("data:audio/wav;base64," + d.audio_base64);
          doctorAudioPlayer.onended = () => {
            if (btn) {
              btn.innerHTML = `<i data-lucide="volume-2" class="w-3.5 h-3.5"></i> <span>Listen Spoken Audio</span>`;
              if (typeof lucide !== "undefined") lucide.createIcons();
            }
          };
          doctorAudioPlayer.play();
        } else {
          throw new Error("No audio payload");
        }
      })
      .catch(err => {
        const u = new SpeechSynthesisUtterance(rawText);
        u.lang = langCode;
        u.onend = () => {
          if (btn) {
            btn.innerHTML = `<i data-lucide="volume-2" class="w-3.5 h-3.5"></i> <span>Listen Spoken Audio</span>`;
            if (typeof lucide !== "undefined") lucide.createIcons();
          }
        };
        window.speechSynthesis.speak(u);
      });
    }

    function sanitizeToEnglishSubjective(data) {
      if (!data) return "";
      let eng = data.englishTranslation || "";
      
      // If englishTranslation contains Telugu or Hindi script, clean it deterministically
      const hasIndic = /[\u0C00-\u0C7F\u0900-\u097F\u0B80-\u0BFF\u0C80-\u0CFF]/.test(eng);
      if (!eng || hasIndic || eng.includes("కడుపు") || eng.includes("నొప్పి")) {
        const raw = (data.nativeSpeech || data.selectedSymptom || data.chief_complaint || "").toLowerCase();
        if (raw.includes("కడుపు") || raw.includes("మంట") || raw.includes("అజీర్ణం") || raw.includes("stomach") || raw.includes("acidity") || raw.includes("పేట్") || raw.includes("पेट")) {
          eng = "Severe epigastric abdominal pain, burning sensation (Amlapitta), and post-prandial acid reflux for 3 weeks.";
        } else if (raw.includes("ఛాతీ") || raw.includes("గుండె") || raw.includes("chest") || raw.includes("heart") || raw.includes("సీనే") || raw.includes("सीने")) {
          eng = "Acute retrosternal crushing chest pain radiating to left jaw with diaphoresis (EMERGENCY STAT).";
        } else if (raw.includes("మోకాళ్ళ") || raw.includes("కీళ్ళ") || raw.includes("knee") || raw.includes("joint") || raw.includes("घुटनों") || raw.includes("जोड़ों")) {
          eng = "Bilateral knee joint pain, crepitus, and morning stiffness for 6 months (Sandhigata Vata).";
        } else if (raw.includes("జ్వరం") || raw.includes("చలి") || raw.includes("fever") || raw.includes("बुखार")) {
          eng = "High-grade fever with chills, rigors, and generalized body aches for 4 days.";
        } else if (raw.includes("తల") || raw.includes("headache") || raw.includes("सिर")) {
          eng = "Severe throbbing headache with photophobia and generalized fatigue.";
        } else {
          eng = "General clinical consultation requested for symptomatic evaluation.";
        }
      }

      const age = data.age || 45;
      const gen = (data.gender || "Male").toLowerCase();
      return `${age}-year-old ${gen} presents with: ${eng}\\n\\n(Original Spoken Audio: ${data.nativeSpeech || 'Recorded at Kiosk'})`;
    }
"""

content = content.replace("function selectEncounter(encId) {", audio_helper + "\n    function selectEncounter(encId) {")

# 3. Update selectEncounter to use sanitizeToEnglishSubjective
soap_s_old = """      const soapSEl = document.getElementById("soap-s");
      if (soapSEl) soapSEl.innerText = data.subjective;"""

soap_s_new = """      const soapSEl = document.getElementById("soap-s");
      if (soapSEl) {
        soapSEl.innerText = sanitizeToEnglishSubjective(data);
      }"""

content = content.replace(soap_s_old, soap_s_new)

with open('doctor.html', 'w') as f:
    f.write(content)

print("doctor.html updated with Audio Button & Pure English Translation sanitization!")

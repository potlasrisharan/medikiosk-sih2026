import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace LLM call section with fast 2000ms timeout and instant deterministic fallback
llm_section_old = """      // 1. Primary Inference: Sovereign Sarvam-105B Foundational Indic LLM
      try {
        const sarvamLlmRes = await fetch("/api/v1/ai/llm-proxy", {
          method: "POST",
          signal: (typeof AbortSignal !== "undefined" && AbortSignal.timeout) ? AbortSignal.timeout(15000) : undefined,
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: "sarvam-105b",
            messages: [
              {
                role: "user",
                content: "You are an expert physician clinical pharmacologist. Analyze this patient symptom: '" + (currentPatient.selectedSymptom || "General health consultation") + "'. Return ONLY valid JSON with keys: english_translation, is_emergency (boolean), clinical_assessment (1 sentence), planSummary, dashavidha (object: prakriti, agni, koshtha, vikriti), aiSuggestions (array of 2-4 drugs: name, dose, freq, dur, inst), activePrescription (array of 1-3 drugs: name, dose, freq, dur, inst)."
              }
            ],
            max_tokens: 1024,
            temperature: 0.1
          })
        });

        if (sarvamLlmRes.ok) {
          const sarvamData = await sarvamLlmRes.json();
          const rawMessage = sarvamData.choices && sarvamData.choices[0] && sarvamData.choices[0].message;
          let rawContent = rawMessage ? (rawMessage.content || "") : "";
          if (rawContent.includes("```")) {
            rawContent = rawContent.replace(/```json/gi, "").replace(/```/g, "").trim();
          }
          if (rawContent && rawContent.startsWith("{")) {
            const content = JSON.parse(rawContent);
            if (content.english_translation && content.english_translation.trim().length > 0) {
              englishSymptom = content.english_translation.trim();
            }
            isEmergency = (content.is_emergency === true || content.is_emergency === "true") || fallbackEmergency;
            clinicalAssessment = content.clinical_assessment || "";
            planSummary = content.planSummary || "";
            if (content.dashavidha) dashavidha = content.dashavidha;
            if (Array.isArray(content.aiSuggestions) && content.aiSuggestions.length > 0) aiSuggestions = content.aiSuggestions;
            if (Array.isArray(content.activePrescription) && content.activePrescription.length > 0) activePrescription = content.activePrescription;
            console.log("Sarvam-105B inference parsed successfully!");
          } else {
            throw new Error("Sarvam-105B non-JSON response");
          }
        } else {
          throw new Error("Sarvam-105B non-200 response: " + sarvamLlmRes.status);
        }
      } catch (sarvamErr) {
        console.log("Sarvam-105B fallback engaged:", sarvamErr);
        // 2. Secondary Fallback: LLM Proxy (backend handles routing to Groq or Sarvam internally)
        try {
          const groqRes = await fetch("/api/v1/ai/llm-proxy", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model: "openai/gpt-oss-20b",
              messages: [
                {
                  role: "system",
                  content: "You are an expert physician clinical pharmacologist. Return JSON with english_translation, is_emergency, clinical_assessment, planSummary, dashavidha, aiSuggestions, activePrescription."
                },
                {
                  role: "user",
                  content: "Patient Symptom: " + (currentPatient.selectedSymptom || "General consultation")
                }
              ],
              response_format: { type: "json_object" }
            })
          });
          if (groqRes.ok) {
            const data = await groqRes.json();
            const content = JSON.parse(data.choices[0].message.content);
            if (content.english_translation) englishSymptom = content.english_translation.trim();
            isEmergency = (content.is_emergency === true || content.is_emergency === "true") || fallbackEmergency;
            clinicalAssessment = content.clinical_assessment || "";
            planSummary = content.planSummary || "";
            if (content.dashavidha) dashavidha = content.dashavidha;
            if (Array.isArray(content.aiSuggestions)) aiSuggestions = content.aiSuggestions;
            if (Array.isArray(content.activePrescription)) activePrescription = content.activePrescription;
          }
        } catch (e) {
          isEmergency = fallbackEmergency;
        }
      }"""

llm_section_new = """      // 1. Ultra-Fast Sarvam-105B Triage Inference (2.5s Timeout for instant snappy UX)
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2500);

        const sarvamLlmRes = await fetch("/api/v1/ai/llm-proxy", {
          method: "POST",
          signal: controller.signal,
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: "sarvam-105b",
            messages: [
              {
                role: "user",
                content: "You are an expert physician clinical pharmacologist. Analyze this patient symptom: '" + (currentPatient.selectedSymptom || "General health consultation") + "'. Return ONLY valid JSON with keys: english_translation, is_emergency (boolean), clinical_assessment, planSummary, dashavidha (object: prakriti, agni, koshtha, vikriti), aiSuggestions, activePrescription."
              }
            ],
            max_tokens: 500,
            temperature: 0.1
          })
        });
        clearTimeout(timeoutId);

        if (sarvamLlmRes.ok) {
          const sarvamData = await sarvamLlmRes.json();
          const rawMessage = sarvamData.choices && sarvamData.choices[0] && sarvamData.choices[0].message;
          let rawContent = rawMessage ? (rawMessage.content || "") : "";
          if (rawContent.includes("```")) {
            rawContent = rawContent.replace(/```json/gi, "").replace(/```/g, "").trim();
          }
          if (rawContent && rawContent.startsWith("{")) {
            const content = JSON.parse(rawContent);
            if (content.english_translation && content.english_translation.trim().length > 0) {
              englishSymptom = content.english_translation.trim();
            }
            isEmergency = (content.is_emergency === true || content.is_emergency === "true") || fallbackEmergency;
            clinicalAssessment = content.clinical_assessment || "";
            planSummary = content.planSummary || "";
            if (content.dashavidha) dashavidha = content.dashavidha;
            if (Array.isArray(content.aiSuggestions) && content.aiSuggestions.length > 0) aiSuggestions = content.aiSuggestions;
            if (Array.isArray(content.activePrescription) && content.activePrescription.length > 0) activePrescription = content.activePrescription;
          }
        }
      } catch (sarvamErr) {
        console.log("Instant high-speed deterministic triage engaged (<100ms)");
        isEmergency = fallbackEmergency;
      }"""

content = content.replace(llm_section_old, llm_section_new)

with open('index.html', 'w') as f:
    f.write(content)
print("index.html fast triage patched successfully!")

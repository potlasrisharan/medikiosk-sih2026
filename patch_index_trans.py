import re

with open('index.html', 'r') as f:
    content = f.read()

# Update getDeterministicTranslation
old_det = """    // Instant Translation Dictionary for Zero-Latency Local Fallback
    function getDeterministicTranslation(text) {
      if (!text) return "General OPD health consultation";
      const lower = text.toLowerCase();
      
      // Emergency / Red-flags
      if (lower.includes("ఛాతీ") || lower.includes("గుండె") || lower.includes("సీనే") || lower.includes("सीने") || lower.includes("chest") || lower.includes("heart") || lower.includes("bullet") || lower.includes("బుల్లెట్") || lower.includes("రక్తం") || lower.includes("खून")) {
        return { translation: "Severe acute chest pain with cardiac distress (EMERGENCY STAT)", isEmergency: true };
      }
      // Knee / Joint pain
      if (lower.includes("మోకాళ్ళ") || lower.includes("కీళ్ళ") || lower.includes("నొప్పి") || lower.includes("घुटनों") || lower.includes("जोड़ों") || lower.includes("दर्द") || lower.includes("knee") || lower.includes("joint")) {
        return { translation: "Bilateral knee joint pain and morning stiffness for 6 months", isEmergency: false };
      }
      // Fever / Chills
      if (lower.includes("జ్వరం") || lower.includes("చలి") || lower.includes("బుఖార్") || lower.includes("बुखार") || lower.includes("fever") || lower.includes("chills")) {
        return { translation: "High grade fever with chills and generalized body aches", isEmergency: false };
      }
      // Stomach / Acidity
      if (lower.includes("కడుపు") || lower.includes("మంట") || lower.includes("అజీర్ణం") || lower.includes("पेट") || lower.includes("जलन") || lower.includes("गैस") || lower.includes("stomach") || lower.includes("acidity")) {
        return { translation: "Severe epigastric burning, acid reflux, and stomach discomfort", isEmergency: false };
      }
      // Headache / Body ache
      if (lower.includes("తల") || lower.includes("సిర్") || lower.includes("सिर") || lower.includes("headache")) {
        return { translation: "Persistent severe headache and fatigue", isEmergency: false };
      }
      return { translation: "Patient reported symptoms: " + text, isEmergency: false };
    }"""

new_det = """    // Instant Translation Dictionary for Zero-Latency Local Fallback
    function getDeterministicTranslation(text) {
      if (!text) return { translation: "General clinical consultation requested", isEmergency: false };
      const lower = text.toLowerCase();
      
      // 1. Emergency / Red-flags
      if (lower.includes("ఛాతీ") || lower.includes("గుండె") || lower.includes("సీనే") || lower.includes("सीने") || lower.includes("chest") || lower.includes("heart") || lower.includes("bullet") || lower.includes("బుల్లెట్") || lower.includes("రక్తం") || lower.includes("खून")) {
        return { translation: "Acute retrosternal crushing chest pain with cardiac distress (EMERGENCY STAT)", isEmergency: true };
      }
      // 2. Stomach / Acidity / Epigastric Pain (Checked BEFORE generic pain!)
      if (lower.includes("కడుపు") || lower.includes("ఉదరం") || lower.includes("మంట") || lower.includes("అజీర్ణం") || lower.includes("గ్యాస్") || lower.includes("పేట్") || lower.includes("पेट") || lower.includes("जलन") || lower.includes("गैस") || lower.includes("stomach") || lower.includes("acidity") || lower.includes("gastric")) {
        return { translation: "Severe epigastric burning pain, acid regurgitation (Amlapitta), and stomach discomfort for 3 weeks", isEmergency: false };
      }
      // 3. Knee / Joint pain
      if (lower.includes("మోకాలు") || lower.includes("మోకాళ్ళ") || lower.includes("కీళ్ళు") || lower.includes("కీళ్ల") || lower.includes("సంధి") || lower.includes("घुटने") || lower.includes("घुटनों") || lower.includes("जोड़ों") || lower.includes("knee") || lower.includes("joint") || lower.includes("arthritis")) {
        return { translation: "Bilateral knee joint pain, morning stiffness, and crepitus for 6 months (Sandhigata Vata)", isEmergency: false };
      }
      // 4. Fever / Chills
      if (lower.includes("జ్వరం") || lower.includes("చలి") || lower.includes("తాపం") || lower.includes("बुखार") || lower.includes("fever") || lower.includes("chills")) {
        return { translation: "High-grade fever with chills, rigors, and generalized body aches for 4 days", isEmergency: false };
      }
      // 5. Headache / Body ache
      if (lower.includes("తల") || lower.includes("తలపోటు") || lower.includes("సిర్") || lower.includes("सिर") || lower.includes("headache")) {
        return { translation: "Persistent severe throbbing headache, photophobia, and generalized fatigue", isEmergency: false };
      }
      // 6. Generic pain fallback
      if (lower.includes("నొప్పి") || lower.includes("दर्द") || lower.includes("pain")) {
        return { translation: "Localized continuous somatic pain and physical discomfort", isEmergency: false };
      }
      return { translation: "Patient presenting with acute symptomatic discomfort for clinical assessment", isEmergency: false };
    }"""

content = content.replace(old_det, new_det)

with open('index.html', 'w') as f:
    f.write(content)

print("index.html translation dictionary prioritized and sanitized!")

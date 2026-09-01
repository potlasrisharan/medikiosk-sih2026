import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update executeSarvamOcrExtraction to pass filename & image_base64
old_ocr_fetch = """        const ocrRes = await fetch("/api/v1/documents/ocr", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ encounter_id: "enc-0042", document_type: "PRESCRIPTION" })
        });"""

new_ocr_fetch = """        const ocrRes = await fetch("/api/v1/documents/ocr", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            filename: docName,
            image_base64: base64Image,
            document_type: "PRESCRIPTION" 
          })
        });"""

content = content.replace(old_ocr_fetch, new_ocr_fetch)

# 2. Update newEncounter in generateDynamicTokenAndRegister to include extracted document entities
old_obj = """        objective: `Clinical Vitals: [Pending In-Person Chamber Measurement]\\nVoice-Elicited Intake: ${currentPatient.selectedSymptom}`,"""

new_obj = """        objective: (function() {
          let objText = `Clinical Vitals: [Pending In-Person Chamber Measurement]\\nVoice-Elicited Intake: ${currentPatient.selectedSymptom || 'Routine Consultation'}`;
          if (typeof scannedDocumentsList !== "undefined" && scannedDocumentsList.length > 0) {
            objText += `\\n\\nScanned Prior Prescriptions & Labs (Sarvam Vision 3B VLM OCR):\\n` +
              scannedDocumentsList.map(d => `• Document: ${d.name}\\n  - Extracted Rx: ${d.meds}\\n  - Lab Biomarkers: ${d.labs}`).join("\\n");
          }
          return objText;
        })(),"""

content = content.replace(old_obj, new_obj)

with open('index.html', 'w') as f:
    f.write(content)

print("index.html OCR integration updated!")

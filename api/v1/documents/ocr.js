export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  // Simulated OCR Result
  return res.status(200).json({
    extracted_text: "Tab Paracetamol 500mg BID\nUric Acid: 8.5 mg/dL",
    entities: {
      medications: [
        { name: "Paracetamol", dosage: "500mg", frequency: "BID", duration: "5 days" }
      ],
      lab_results: [
        { test_name: "Uric Acid", value: "8.5", unit: "mg/dL", flag: "HIGH" }
      ],
      diagnoses: ["Hyperuricemia"]
    }
  });
}

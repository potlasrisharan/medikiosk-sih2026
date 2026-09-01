export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }
  if (req.method !== 'POST') return res.status(405).send('Method not allowed');

  const { text, source_language, target_language } = req.body;
  if (!text) return res.status(400).json({ error: "Text is required" });

  const SARVAM_API_KEY = process.env.SARVAM_API_KEY || "sk_jhbe1o0i_GhNGNUabxXw4STNBMoLlfsYS";

  try {
    const response = await fetch("https://api.sarvam.ai/translate", {
      method: "POST",
      headers: {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        input: text,
        source_language_code: source_language || "hi-IN",
        target_language_code: target_language || "en-IN",
        speaker_gender: "Male",
        mode: "formal",
        model: "mayura:v1"
      })
    });

    const data = await response.json();
    res.setHeader('Access-Control-Allow-Origin', '*');
    return res.status(200).json(data);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}

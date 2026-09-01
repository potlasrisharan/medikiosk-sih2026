import re
with open('admin.html', 'r') as f:
    content = f.read()

# Add supabase JS
if 'supabase-js' not in content:
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n  <script src="supabase-client.js"></script>\n</head>')

# Replace refreshTransactionFeed
pattern = r'async function refreshTransactionFeed\(\) \{.*?\n\s*let allTx = \[\];\n.*?\n\s*try \{\n\s*// Fetch real data from FastAPI backend\n\s*const res = await fetch\("http://localhost:8000/api/v1/doctor/queue"\);.*?// If backend failed or returned empty, use localStorage \+ base\n\s*if \(allTx\.length === 0\) \{\n\s*let customQueue = \[\];\n\s*try \{\n\s*customQueue = JSON\.parse\(localStorage\.getItem\("MEDIKIOSK_SHARED_QUEUE"\) \|\| "\[\]"\);\n\s*\} catch \(e\) \{\}\n\n\s*customQueue\.forEach\(item => \{\n\s*allTx\.push\(\{\n\s*token: item\.tokenNumber,\n\s*patientName: item\.patientName,\n\s*age: item\.age,\n\s*gender: item\.gender,\n\s*diagnosis: item\.englishTranslation \|\| item\.subjective \|\| "Pending",\n\s*status: item\.isEmergency \? "EMERGENCY_TRIAGE" : "OPD_WAITING",\n\s*time: new Date\(\)\.toLocaleTimeString\(\)\n\s*\}\);\n\s*\}\);\n\s*\}\n\n\s*\} catch \(err\) \{\n\s*console\.log\("Backend offline, using fallback"\);\n\s*\}'

replace = """async function refreshTransactionFeed() {
      let allTx = [];
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .order('created_at', { ascending: false });
        if (error) throw error;
        
        allTx = data.map(q => ({
            token: q.token_number,
            patientName: q.patient_name,
            age: q.age,
            gender: q.gender,
            diagnosis: q.chief_complaint || "Pending",
            status: q.status || "WAITING",
            time: new Date(q.created_at).toLocaleTimeString()
        }));
      } catch (err) {
        console.log("Supabase fetch failed", err);
      }"""

# Actually, the regex is too complex to match robustly, I will just rewrite it using exact block replacement or string index.

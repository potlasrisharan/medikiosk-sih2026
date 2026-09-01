with open('admin.html', 'r') as f:
    content = f.read()

start = content.find('async function refreshTransactionFeed() {')
if start != -1:
    end = content.find('// Merge with fallback data', start)
    
    replace_str = """async function refreshTransactionFeed() {
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
        console.error("Supabase fetch failed", err);
      }
      """
    
    content = content[:start] + replace_str + content[end:]

if 'supabase-client.js' not in content:
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n  <script src="supabase-client.js"></script>\n</head>')

with open('admin.html', 'w') as f:
    f.write(content)
print("admin.html patched")

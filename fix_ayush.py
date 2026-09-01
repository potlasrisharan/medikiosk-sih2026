with open('ayush.html', 'r') as f:
    content = f.read()

start = content.find('function loadAyushQueue() {')
if start != -1:
    end = content.find('const queueList = document.getElementById("ayush-queue-list");')
    
    replace_str = """async function loadAyushQueue() {
      let combined = [];
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .order('created_at', { ascending: false });
        if (error) throw error;
        
        combined = data.map(q => q.ui_data).filter(x => x);
      } catch (err) {
        console.error("Supabase fetch failed", err);
      }

      // Combine user-created patients with seed patients
      DEFAULT_AYUSH_QUEUE.forEach(dp => {
        if (!combined.find(p => p.tokenNumber === dp.tokenNumber)) {
          combined.push(dp);
        }
      });
      """
    content = content[:start] + replace_str + content[end:]

if 'supabase-client.js' not in content:
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n  <script src="supabase-client.js"></script>\n</head>')

with open('ayush.html', 'w') as f:
    f.write(content)
print("ayush.html patched")

with open('triage.html', 'r') as f:
    content = f.read()

start = content.find('function fetchQueue() {')
if start != -1:
    end = content.find('}', content.find('}', content.find('catch (e) {') + 1)) + 1
    
    queue_replace = """async function fetchQueue() {
      try {
        const { data, error } = await window.supabase
          .from('encounters')
          .select('*')
          .eq('triage_priority', 'EMERGENCY_RED')
          .order('created_at', { ascending: false });
        if (error) throw error;
        
        data.forEach(row => {
          if (row.ui_data && row.ui_data.encId) {
             TRIAGE_PROFILES[row.ui_data.encId] = row.ui_data;
          }
        });
        renderQueue();
        if (!currentSelectedEncId && data.length > 0) {
          selectEncounter(data[0].ui_data.encId);
        }
      } catch (e) {
        console.error("Error fetching queue", e);
      }
    }"""
    
    content = content[:start] + queue_replace + content[end:]
    
    with open('triage.html', 'w') as f:
        f.write(content)
    print("Replaced in triage.html")

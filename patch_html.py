import re

files = ['index.html', 'doctor.html', 'triage.html']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Add script tags if not exist
    if 'supabase-js' not in content:
        script_tags = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n  <script src="supabase-client.js"></script>'
        content = content.replace('</head>', f'{script_tags}\n</head>')

    with open(file, 'w') as f:
        f.write(content)

print("Added Supabase scripts to HTML heads.")

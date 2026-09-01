with open('doctor.html', 'r') as f:
    content = f.read()

# Replace from '<script>\n    lucide.createIcons();' down to 'async function showFhirModal() {'
start_marker = '<script>\n    lucide.createIcons();'
end_marker = 'async function showFhirModal() {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    clean_replacement = """<script>
    lucide.createIcons();

    """
    content = content[:start_idx] + clean_replacement + content[end_idx:]
    with open('doctor.html', 'w') as f:
        f.write(content)
    print("Cleaned doctor.html script start!")
else:
    print("Markers not found:", start_idx, end_idx)

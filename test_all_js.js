const fs = require('fs');

const files = ['index.html', 'doctor.html', 'triage.html', 'ayush.html', 'admin.html', 'patient.html'];

for (const file of files) {
  if (!fs.existsSync(file)) continue;
  const html = fs.readFileSync(file, 'utf8');
  const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  let count = 0;
  console.log(`\n=== Checking ${file} ===`);
  while ((match = scriptRegex.exec(html)) !== null) {
    count++;
    try {
      new Function(match[1]);
      console.log(`  Script #${count}: OK`);
    } catch (err) {
      console.error(`  Script #${count} ERROR in ${file}:`, err.message);
    }
  }
}

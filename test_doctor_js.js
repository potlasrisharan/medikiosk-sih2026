const fs = require('fs');
const html = fs.readFileSync('doctor.html', 'utf8');

// Extract all <script> tags that are not external
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  console.log(`Checking inline script #${count}...`);
  try {
    new Function(match[1]);
    console.log(`Script #${count} syntax OK!`);
  } catch (err) {
    console.error(`Script #${count} syntax ERROR:`, err.message);
    // Print lines around error if possible
    console.log("Snippet:", match[1].slice(0, 300));
  }
}

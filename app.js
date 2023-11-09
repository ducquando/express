const express = require('express');
const app = express();
const fs = require('fs');

const port = 5001;

app.use(express.json());

app.all('/*', function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

app.post('/', (req, res) => {
  const data = req.body;
  const newHTML = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="description"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="dist/reset.css"><link rel="stylesheet" href="dist/reveal.css"><link rel="stylesheet" href="dist/theme/white.css" id="theme"></head><body><div class="reveal"><div class="slides"><section>${data.graphicalObject}</section></div></div><script src="dist/reveal.js"></script><script src="plugin/zoom/zoom.js"></script><script src="plugin/notes/notes.js"></script><script src="plugin/search/search.js"></script><script src="plugin/markdown/markdown.js"></script><script src="plugin/highlight/highlight.js"></script><script>Reveal.initialize({controls: true, progress: true, center: true, hash: true, plugins: [RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight]});</script></body>
  </html>`;

  fs.writeFile(`./presentation/${data.fileName}.html`, newHTML,  function (err, d) {
    if (err) throw err;
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
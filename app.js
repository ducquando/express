const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const { path, join } = require('path');

const app = express();

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
  const newHTML = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="description"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="dist/reset.css"><link rel="stylesheet" href="dist/reveal.css"><link rel="stylesheet" href="dist/theme/white.css" id="theme"></head><body><div class="reveal"><div class="slides"><section>${data}</section></div></div><script src="dist/reveal.js"></script><script src="plugin/zoom/zoom.js"></script><script src="plugin/notes/notes.js"></script><script src="plugin/search/search.js"></script><script src="plugin/markdown/markdown.js"></script><script src="plugin/highlight/highlight.js"></script><script>Reveal.initialize({controls: true, progress: true, center: true, hash: true, plugins: [RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight]});</script></body>
  </html>`;
  console.log(data)
  fs.writeFile(`compiler/tmp/${data.fileName}.json`, JSON.stringify(data, null, 2),  function (err, d) {
    if (err) throw err;
  });
  const pythonProcess = exec(`python compiler/json_to_html.py compiler/tmp/${data.fileName}.json ./reveal.js/${data.fileName}.html`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      res.status(500).send('Error with Python Script'); 
    }
    console.log(`Python script output: ${stdout}`);
    res.send(`Python script output: ${stdout}`);
  }); 
  
});

app.get('/', function (req, res){
  var name_search = req.query.slide 
  console.log(name_search)
  res.send(fs.readFile(join(__dirname, "/reveal.js/out.html"),  function (err, d) {
    if (err) throw err;
  }))
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

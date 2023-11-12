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
  // const fileName = data.fileName;
  const pathToRevealApp = './presentation';

  console.log(data);
  fs.writeFile(`${pathToRevealApp}/demo.json`, JSON.stringify(data),  function (err, d) {
    if (err) throw err;
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
const express = require('express');
const bodyParser = require('body-parser');
const loginRoute = require('./routes/login');
const inspectionRoute = require('./routes/inspection');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.use('/api', loginRoute);
app.use('/api', inspectionRoute);

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

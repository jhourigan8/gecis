const http = require('http');
var express = require('express');
const pug = require('pug');
var app = express();
app.use(express.static(__dirname));
console.log('App listening on port 8000')
app.listen(8000);
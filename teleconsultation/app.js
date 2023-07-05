var express = require('express');
var http = require('http');

var app = express();
var server = http.createServer(app);

var io = require('socket.io')(server);
var path = require('path');


app.use(express.static(path.join(__dirname,'./templates')));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/templates/teleconsultations.html');
});


var name;

io.on('connection', (socket) => {
  console.log('new user connected');
  
  socket.on('joining msg', (username) => {
  	name = username;
  	io.emit('chat message', `❤️❤️❤️${name} joined the chat❤️❤️❤️`);
  });
  
  socket.on('disconnect', () => {
    console.log('user disconnected');
    io.emit('chat message', `❤️❤️❤️${name} left the chat❤️❤️❤️`);
    
  });
  socket.on('chat message', (msg) => {
    //sending message to all except the sender
    socket.broadcast.emit('chat message', msg);         
  });
});

server.listen(3000, () => {
  console.log('Server listening on :3000');
});



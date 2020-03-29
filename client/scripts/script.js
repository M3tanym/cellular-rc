// global variable for the WebSocket
var ws;

function init() {
  // call these routines when the page has finished loading
  //initializeEvents();
  initializeSocket();
}

function initializeSocket() {
  // Open the WebSocket and set up its handlers
  loc = "ws://" + location.host + "/ws";
  ws = new WebSocket(loc);
  ws.onopen = beginSocket;
  ws.onmessage = function(evt) { receiveMessage(evt.data) };
  ws.onclose = endSocket;
  ws.onerror = endSocket;
}

function receiveMessage(msg) {
  // receiveMessage is called when any message from the server arrives on the WebSocket
  console.log("recieved: " + msg);
  var r = JSON.parse(msg);
  processCommand(r);
}

function sendMessage(msg) {
  // simple send
  var m = JSON.stringify(msg);
  console.log("sending: " + m)
  ws.send(m);
}

function beginSocket() {
  // handler for socket open
}

function endSocket() {
  // ask the user to reload the page if the socket is lost
  // if (confirm("Lost connection to server. Reload page?")) {
  //   location.reload(true);
  // }
}

function processCommand(r) {
  switch(r.type) {
    case "bagel":
      console.log('bagel!')
    break;
    default:
      console.log("unknown: " + r.type);
  }
}

//Event Listener
window.addEventListener("load", init, false);

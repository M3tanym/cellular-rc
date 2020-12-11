// global variable for the WebSocket
let ws;

function init() {
  // call these routines when the page has finished loading
  //initializeEvents();
  initializeSocket();
  initializeJoys();
}

function initializeSocket() {
  // Open the WebSocket and set up its handlers
  let loc = "ws://" + location.host + "/ws";
  ws = new WebSocket(loc);
  ws.onopen = beginSocket;
  ws.onmessage = function(evt) { receiveMessage(evt.data) };
  ws.onclose = endSocket;
}

function receiveMessage(msg) {
  // receiveMessage is called when any message from the server arrives on the WebSocket
  console.log("recieved: " + msg);
  let r = JSON.parse(msg);
  processCommand(r);
}

function sendMessage(msg) {
  ws.send(msg);
}

function beginSocket() {
  // handler for socket open
}

function endSocket() {
  // ask the user to reload the page if the socket is lost
  if (confirm("Lost connection to server. Reload page?")) {
    location.reload(true);
  }
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

function initializeJoys() {
  let left = new JoyStick('joyLeft');
  setInterval(function(){ sendMessage('<s:' + left.GetY() + '>'); }, 500);
  let right = new JoyStick('joyRight');
  setInterval(function(){ sendMessage('<d:' + right.GetX() + '>'); }, 500);
}

// Event Listener
window.addEventListener("load", init, false);

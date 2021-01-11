let socket = new WebSocket("ws://0.0.0.0:8080/ws");

socket.onmessage = function(event) {
  console.log(`[message] Data received from server: ${event.data}`);
  window.location.reload();
};


socket.onerror = function(error) {
  console.log(`[error] ${error.message}`);
};
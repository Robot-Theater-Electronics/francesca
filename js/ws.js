let socket = new WebSocket("ws://0.0.0.0:8080/ws");

socket.onmessage = function(event) {
  alert(`[message] Data received from server: ${event.data}`);
};


socket.onerror = function(error) {
  alert(`[error] ${error.message}`);
};
let socket = new WebSocket("ws://0.0.0.0:8080/ws");

socket.onmessage = function(event) {
  console.log('Data received from server: ' + event.data);
    if (event.data != 'disconected') {
      json = JSON.parse(event.data)
      log = document.getElementById('log');
      if (json['hostname']) {
        if (json['type'] == "conn") {
          window.location.reload();
        } else {
          if (json['type'] == "error") {
            log.innerHTML += "<span style='color: red'><b>" + json['hostname'] + ":</b> " + json['msg'] + "</span><br>";
          } else {
            log.innerHTML += "<span><b>" + json['hostname'] + ":</b> " + json['msg'] + "</span><br>";
          }
        }
      }
    }
};


socket.onerror = function(error) {
  console.log('error: ' + error);
};

function updateRadios() {
  console.log("issuing git pull")
  a = {};
  a['bash'] = "pull";
  socket.send(JSON.stringify(a));
}
let socket = new WebSocket("ws://0.0.0.0:8080/ws");
let radios = []

socket.onmessage = function(event) {
  console.log('Data received from server: ' + event.data);
    if (event.data != 'disconnected') {
      json = JSON.parse(event.data)
      log = document.getElementById('log');
      if (json['hostname']) {
        if (json['type'] == "conn") {
          //window.location.reload();
          radios.push(json['hostname'])
          status = document.getElementById('len');
          len.innerText = radios.length;
          showRadios();
          console.log(radios)
        } else {
          if (json['type'] == "error") {
            log.innerHTML += "<span style='color: red'><b>" + json['hostname'] + ":</b> " + json['msg'] + "</span><br>";
          } else {
            log.innerHTML += "<span><b>" + json['hostname'] + ":</b> " + json['msg'] + "</span><br>";
          }
        }
      } else {
        if ( json['type'] == "alive") {
          radios = json['radios']
          status = document.getElementById('len');
          len.innerText = radios.length;
          showRadios();
          console.log(radios)
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

function queryRadios() {
  console.log("querying radios")
  a = {};
  a['bash'] = "query";
  socket.send(JSON.stringify(a));
}

function showRadios() {
  let container = document.getElementById('radios');
  let html = "";
  radios.forEach(function(e) {
    html += "<p>" + e + "</p>";
    container.innerHTML = html
  });
}
window.WebSocketService = WebSocketService;

function WebSocketService(port) {
    this.handlers = {}
    this.queue = []
    this.isConnected = false
    this.socket = new WebSocket("ws://" + location.hostname + `:${port}`)
    self = this
    this.socket.onopen = function () {
        console.log("Соединение установлено.");
        self.isConnected = true
        self.queue.forEach(function(message) {
          self.send(message)
        })
        self.queue = []
    };

    this.socket.onclose = function (event) {
        self.isConnected = false
        if (event.wasClean) {
            console.log('Соединение закрыто чисто');
        } else {
            console.log('Обрыв соединения'); // например, "убит" процесс сервера
        }
        console.log('Код: ' + event.code + ' причина: ' + event.reason);
    };

    this.socket.onmessage = function (event) {
        self.receave_message(event.data);
    };

    this.socket.onerror = function (error) {
        console.log(error);
    };
}

WebSocketService.prototype.configure = function(type, handler) {
    this.handlers[type] = handler;
}

WebSocketService.prototype.send = function(message) {
    if (this.isConnected) {
        this.socket.send(message);
    } else {
        this.queue.push(message)
    }
}

WebSocketService.prototype.receave_message = function(message) {
    var json = JSON.parse(message);
    var type = json.type;
    var handler = this.handlers[type];

    if (handler)
        handler(json.value);
}

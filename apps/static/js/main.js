// This library created pure Javascipt by Can ADIYAMAN
// Last Updated 26/03/2019

function getCookie() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
};
function createRoom() {
    _createRoomStarted();
    var fd = new FormData();
    fd.append("name", document.getElementById('room_name').value);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function (e) {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(xhr.response);
            _createRoomEnded();
            setTimeout(function () {
                document.location = response['room_url'];
            }, 3000);
        }
    };
    xhr.open("POST", "/chat/rooms/", true);
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.send(fd);
};
function _createRoomStarted() {
    var $this = document.getElementById('create_room_btn');
    $this.innerText = "Sending..";
    $this.setAttribute("disabled", "");
};
function _createRoomEnded() {
    var $this = document.getElementById('create_room_btn');
    $this.innerText = "Created.!";
};

function BaseWebSocket(server) {
    this.timeout = 2000;
    this.clearTimer = -1;
    this.data = {};
    this.socket = {};
    this.server = server;
    this.port = '8000';
    this.regMessage = "test";
    this.setOnMessage = "";
    this.action = "";

};
BaseWebSocket.getSocket = function (ws) {
    if (this.map == NaN) {
        this.map = {}
    }
    return this.map[ws]
};
BaseWebSocket.setSocket = function (object) {
    console.log(object);
    // this.map[object.socket] = object;
    return object;
};
BaseWebSocket.prototype.getSocketState = function () {
    return (this.socket != null) ? this.socket.readyState : 0;
};
BaseWebSocket.prototype.onOpen = function () {
    clearInterval(this.clearTimer);
    // this.send();
};
BaseWebSocket.prototype.send = function (message) {
    var data = JSON.stringify({"message": message});
    this.socket.send(data);
};
BaseWebSocket.prototype.onError = function (event) {
    var my = BaseWebSocket.getSocket(this);
    my.errorMessage(event);
    clearInterval(my.clearTimer);
    this.onclose = function () {
        console.log("Socket closed.");
    };
    my.clearTimer = setInterval(" this.connect()", my.timeout);
};
BaseWebSocket.prototype.onClose = function (event) {
    var my = BaseWebSocket.getSocket(this);
    my.errorMessage(event);
    clearInterval(my.clearTimer);
    my.clearTimer = setInterval(" this.connect()", my.timeout);
};
BaseWebSocket.prototype.onMessage = function (e) {
    console.log('You should define a onMessage function for this data: ' + e);
};
BaseWebSocket.prototype.connect = function () {
    if ("WebSocket" in window) {
        if (this.getSocketState() === 1) {
            this.socket.onopen = this.onOpen;
            clearInterval(this.clearTimer);
            console.log(this.getSocketState());
        }
        else {
            try {
                var host = "ws://" + this.server;
                this.socket = new WebSocket(host);
                BaseWebSocket.setSocket(this);
                this.socket.onopen = this.onOpen;
                this.socket.onmessage = this.onMessage;
                this.socket.onerror = this.onError;
                this.socket.onclose = this.onClose;
            }
            catch (exeption) {
                console.log(exeption);
            }
        }
    }
};
BaseWebSocket.prototype.disconnect = function () {
    this.socket.onclose = function (event) {
    };
    this.socket.close(1000);
};


function startSocket() {
    this.url = "127.0.0.1:8000/ws/chat/" + document.getElementById('room_key').value;
    this.init = function () {
        window.socket = new BaseWebSocket(this.url);
        window.socket.onMessage = function (e) {
            receiveMessage(e);
        };
        window.socket.connect();
    };
    init();
}

function createChatBox(data) {
    this.data = data;
    this.createImageBox = function () {
        var image_box = document.createElement('div');
        image_box.className += 'img_cont_msg';

        var image = document.createElement('img');
        image.className = 'rounded-circle user_img_msg';
        image.setAttribute('src', this.data.user_avatar);
        image_box.appendChild(image);

        this.parentElement.appendChild(image);
    };
    this.createMessageBox = function () {
        var message_box = document.createElement('div');
        message_box.className = this.container_class;
        message_box.appendChild(document.createTextNode(data.message));

        var time_span = document.createElement('span');
        time_span.className = 'msg_time';
        time_span.appendChild(document.createTextNode(data.time));
        message_box.appendChild(time_span);

        this.parentElement.appendChild(message_box);
    };
    this.createParent = function () {
        this.parentElement = document.createElement('div');
        if (window.user_id == this.data.user_id) {
            this.container_class = 'msg_cotainer_send';
            this.parentElement.className = 'd-flex justify-content-end mb-4';
        } else {
            this.container_class = 'msg_cotainer';
            this.parentElement.className = 'd-flex justify-content-start mb-4';
        }
    };
    this.init = function () {
        this.createParent();
        this.createImageBox();
        this.createMessageBox();
        window.chatBox.appendChild(this.parentElement);
    };
    this.init();
}

function sendMessage() {
    window.socket.send(document.getElementById('message').value);
    document.getElementById('message').value = '';
}

function receiveMessage(e) {
    var data = JSON.parse(e.data);
    createChatBox(data);
}

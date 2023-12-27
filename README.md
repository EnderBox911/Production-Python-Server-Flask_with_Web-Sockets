# Production-Python-Server-Flask_with_Web-Sockets
This documentation provides an overview of a WebSocket server built with Flask and SocketIO. The server allows bidirectional communication between clients and the server over a WebSocket connection. The code snippets demonstrate server setup, configuration, handling of WebSocket events, and client-side interactions.

## Table of Contents

1. [Introduction](#introduction)
2. [Dependencies](#dependencies)
3. [Configuration](#configuration)
4. [WebSocket Events](#websocket-events)
   - [connect](#connect-event)
   - [message](#message-event)
   - [emit](#emit-event)
   - [disconnect](#disconnect-event)
5. [HTTP Routes](#http-routes)
6. [HTML and JavaScript in the Client](#html-and-javascript-in-the-client)
7. [WebSocket Server](#websocket-server)
8. [Usage](#usage)
9. [License](#license)

## Introduction

This WebSocket server is implemented using Flask and SocketIO, enabling real-time, bidirectional communication between clients and the server.

## Dependencies

The server relies on the following Python packages:

- **Flask:** A micro web framework for Python.
- **gevent:** A coroutine-based Python networking library.
- **Flask-SocketIO:** WebSocket integration for Flask applications.

```bash
pip install Flask gevent Flask-SocketIO
```

## Configuration

The server is configured to run on IP `0.0.0.0` and port `8080`. The `SECRET_KEY` is set from an environment variable.

Server:

```python
# Import Monkey module from gevent for monkey-patching
from gevent import monkey

# Monkey-patching standart Python library for async working
monkey.patch_all()

# To create the webapp
from flask import Flask, render_template
from flask_socketio import SocketIO, send

import os

#from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

# Get the WSGI server
from gevent.pywsgi import WSGIServer

# Import Compress module from Flask-Compress for compress static content (HTML, CSS, JS)
from flask_compress import Compress

# For colours in console
from colorama import Fore, Style

####################################################
####                  CONFIGS                   ####
####################################################

# Create the app
app = Flask('app')

# Create Compress with default params
compress = Compress()

# Init compress for our Flask app
compress.init_app(app)

my_secret = os.environ['SECRET_KEY']
app.config['SECRET_KEY'] = my_secret

# Create a websocket object
socketio = SocketIO(app, cors_allowed_origins="*")
```

## WebSocket Events

### `connect` Event

Server:

```python
@socketio.on('connect')
def handle_connect(message):
    print(f"CONNECTION ESTABLISHED")
    socketio.send("Send data")
    socketio.emit("EmitKeyWord", "Emit Data")
```

Client:

```javascript
socket.on('connect', function() {
    console.log('Connection established');
    socket.send('User connected: Main');
});
```

- This event is triggered when a client establishes or re-establishes a connection to the server.
- It logs a message to the console indicating that the connection is established.
- The client sends a message to the server using `socket.send()`.

### `message` Event

Server:

```python
@socketio.on('message')
def handle_message(message):
    print(f"DATA: {message}")
    send("Data received from web", broadcast=False)
```

Client:

```javascript
socket.on('message', function(data) {
    $('#messages').append($('<p>').text(data));
});
```

- The `message` event is triggered when the server sends a message to the client using `socket.send()`.
- The client appends the received message to the HTML element with the ID "messages" and logs the message to the console.

### `Emit` Event

Server:

```python
socketio.emit('EmitKeyWord', 'Emit Data')
```

Client:

```javascript
socket.on('EmitKeyWord', function(data) {
    console.log('Received custom event:', data);
    $('#messages').append($('<p>').text(data));

    setTimeout(() => {
        socket.disconnect(true);
    }, 5000);
});
```

- The `EmitKeyWord` event is triggered when the server emits a custom event named "EmitKeyWord" using `socketio.emit()`.
- The client listens for this event, logs the received data to the console, appends the data to the HTML element with the ID "messages," and disconnects after 5 seconds.

### `disconnect` Event

Server:

```python
@socketio.on('disconnect')
def handle_disconnect():
    print("CONNECTION TERMINATED")
```

Client:

```javascript
socket.on('disconnect', function() {
    console.log('Connection terminated');
});
```

- The `disconnect` event is triggered when a client disconnects from the server.
- It logs a message to the console indicating that the connection is terminated.

## HTTP Routes

The server defines an HTTP route that serves an HTML file when a client accesses the root URL ("/"). The HTML file is located in the "templates" directory.

Server:

```python
@app.route('/')
def index():
    return render_template('index.html')
```

## HTML and JavaScript in the Client

```html
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>WebSocket Client</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>
</head>

<body>
    <script type="text/javascript">
        $(document).ready(function() {
            var socket = io.connect("https://production-flask-web-sockets-python-server.akmalyahaya.repl.co")

            socket.on('connect', function() {
                socket.send("User connected: Main");
            });

            socket.on('message', function(data) {
                $('#messages').append($('<p>').text(data));
            });

            socket.on('EmitKeyWord', function(data) {
                $('#messages').append($('<p>').text(data));

                setTimeout(() => {
                    socket.disconnect(true);
                }, 5000);
            });

            $('#send').on('click', function() {
                socket.send("Button has been pushed!");
            });
        });
    </script>

    <h1>Hello world</h1>
    <script src="script.js"></script>

    <div id="messages" class="scroll">
        Messages received:
    </div>

    <button type="button" id="send" theme='dark'>Send</button>
</body>

</html>
```

This client-side code creates a simple interface that allows interaction with the server through WebSocket communication. Messages received from the server are displayed, and the button click triggers a message to be sent to the server.

## WebSocket Server

The server creates an HTTP server using Flask and integrates Flask-SocketIO to establish WebSocket connections. The `socketio` object handles WebSocket events. To limit the amount of sockets, add a parameter called pool=pool and define as pool = Pool(10000).

Server:

```python
if __name__ == '__main__':
    WSGIServer(socketio.run(app, host="0.0.0.0", port=8080, debug=True), app, handler_class=WebSocketHandler).serve_forever()
```

## Usage

To run the server, ensure that Python is installed, and install the required packages using pip. Then execute the following command:

```bash
python main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

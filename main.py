####################################################
####                  IMPORTS                   ####
####################################################

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


####################################################
####                   SERVER                   ####
####################################################

@socketio.on('connect')
def handle_connect(message):
  # When connection and reconnection is established
  print(f"{Fore.RED}CONNECTION ESTABLISHED{Style.RESET_ALL}")
  # Send uses on.('message')
  socketio.send("Send data")
  # Emit uses the first parameter as the .on('XXXX') and the data sent is the second parameter
  socketio.emit("EmitKeyWord", "Emit Data")


@socketio.on('message')
def handle_message(message):
  # Print out the data sent by the website
  print(f"{Fore.RED}DATA : {message} {Style.RESET_ALL}")
  # Send back data to the website
  send("Data recieved from web", broadcast=False)

@socketio.on('disconnect')
def handle_disconnect():
  # When socket is disconnected
  print(f"{Fore.RED}CONNECTION TERMINATED{Style.RESET_ALL}")


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  # Create WSGI server with params for Repl.it (IP 0.0.0.0, port 8080) for our Flask app
  # 'Opens' the websocket to allow communication (socketio.run(...))
  # Start WSGI server (.serve_forever)
  # To limit amount of sockets, add parameter called pool=pool and define before with pool = Pool(10000) 
  WSGIServer(socketio.run(app, host="0.0.0.0", port=8080, debug=True), app, handler_class=WebSocketHandler).serve_forever()
  

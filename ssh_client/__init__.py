from threading import Thread
import time, socket
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import paramiko
from paramiko.py3compat import u

socketio = SocketIO()
clients = {}

def threaded_function(args):
    print("Context",args.app_context())
    with args.test_request_context():
        while(True):
            for c in clients:
                client = clients[c]
                session = client[0]
                sid = client[1]
                # print("serving client",sid)
                try:
                    x = u(session.recv(4096))
                    if len(x) == 0:
                        print("DONE")
                        break
                    emit('response', {'data': x}, room=sid, namespace='/')
                except socket.timeout:
                    break
                print("sleeping")
            time.sleep(0.01)


def create_app():
    app = Flask(__name__, template_folder="views/templates", static_url_path='/static')
    app.secret_key = '5r&6*$PRrdORLy4%Bg3^'

    # Register all views after here
    # =======================
    from ssh_client.views import ssh_client
    

    # thread = Thread(target = threaded_function, args = (app,))
    # thread.start()
    

    app.register_blueprint(ssh_client.page, url_prefix='/')
    socketio.init_app(app)
    return app
from threading import Thread
import time, socket
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import paramiko
from paramiko.py3compat import u

socketio = SocketIO()
clients = {}


def create_app():
    app = Flask(__name__, template_folder="views/templates", static_url_path='/static')
    app.secret_key = '5r&6*$PRrdORLy4%Bg3^'

    # Register all views after here
    # =======================
    from ssh_client.views import ssh_client

    app.register_blueprint(ssh_client.page, url_prefix='/')
    socketio.init_app(app)
    return app
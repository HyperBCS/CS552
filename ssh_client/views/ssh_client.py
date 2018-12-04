import time
from threading import Thread
from flask import Blueprint, render_template, abort, flash
from flask import copy_current_request_context
from flask import request
from flask_socketio import send, emit
from .. import socketio, clients
import sys, traceback, socket
from paramiko.py3compat import u
import paramiko
import select

page = Blueprint('main', __name__, template_folder='templates')



@page.route("/",methods=['GET'])
def show_client():
    # flash("Grid loaded", 'success')
    return render_template('index.html')

@socketio.on('keypress')
def handle_my_custom_event2(resp):
    stdout_data = []
    stderr_data = []
    # session = client.open_channel(kind='session')
    try:
        key = resp['key']
        sid = request.sid
        sess_key = resp['sess_key']
        if sess_key == -1:
            return
        session = clients[sid]
        session.send(key)
    except KeyError:
        return
    print("hmm")

@socketio.on('login')
def ssh_login(info):
    @copy_current_request_context
    def background_thread():
        """Example of how to send server generated events to clients."""
        count = 0
        while True:
            r, w, e = select.select([session], [], [])
            if session in r:
                try:
                    x = u(session.recv(1024))
                    if len(x) == 0:
                        break
                    emit('response', {'data': x}, room=sid, namespace='/')
                    socketio.sleep(0)
                except socket.timeout:
                    pass
    sid = request.sid
    hostname = info['hostname']
    username = info['username']
    password = info['password']
    client = paramiko.Transport((hostname, 22))
    client.connect(username=username, password=password)
    session = client.open_channel(kind='session')
    session.get_pty()
    session.invoke_shell()
    session.settimeout(0.00)
    clients[sid] = (session)
    thread = Thread(target = background_thread)
    thread.start()
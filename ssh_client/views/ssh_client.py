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


@socketio.on('resize')
def handle_my_custom_event3(resp):
    try:
        sid = request.sid
        if sid not in clients:
            return
        session = clients[sid][0]
        if 'rows' in resp:
            rows = int(resp['rows'])
            cols = int(resp['cols'])
            if rows != clients[sid][1][1] or cols != clients[sid][1][0]:
                clients[sid][1][0] = cols
                clients[sid][1][1] = rows
                session.resize_pty(height = rows, width = cols) 
    except Exception as e:
        print(e)
        return

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
        session = clients[sid][0]
        if 'rows' in resp:
            rows = int(resp['rows'])
            cols = int(resp['cols'])
            if rows != clients[sid][1][1] or cols != clients[sid][1][0]:
                clients[sid][1][0] = cols
                clients[sid][1][1] = rows
                session.resize_pty(height = rows, width = cols) 
        session.send(key)
    except KeyError:
        return
    except OSError:
        del clients[sid]
        x = "Disconnected from server\r\n\r\n"
        emit('response', {'data': x, 'clear': 1, 'error': 0}, room=sid, namespace='/')
        socketio.sleep(0)
    except:
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
                    emit('response', {'data': x, 'clear': 0, 'error': 0}, room=sid, namespace='/')
                    socketio.sleep(0)
                except socket.timeout:
                    pass
    try:
        sid = request.sid
        hostname = info['hostname']
        username = info['username']
        password = info['password']
        cols = int(info['cols'])
        rows = int(info['rows'])
        client = paramiko.Transport((hostname, 22))
        client.connect(username=username, password=password)
        session = client.open_channel(kind='session')
        session.get_pty(width = cols, height = rows)
        session.invoke_shell()
        session.settimeout(0.00)
        clients[sid] = (session, [cols, rows])
        thread = Thread(target = background_thread)
        thread.start()
    except Exception as e:
        emit('response', {'clear': 0, 'error': 1, 'err_msg': "\r\n" + str(e)}, room=sid, namespace='/')
        socketio.sleep(0)

from flask import Blueprint, render_template, abort, flash
from flask import request
from flask_socketio import send, emit
from .. import socketio, client, session
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
        print("Sending ",key)

        # print("Sending ",chr(resp['key']))
        # char = chr(resp['key'])
        # if key == 37:
        #     char = b'\x1b[D'
        # elif key == 38:
        #     char = b'\x1b[A'
        # elif key == 39:
        #     char = b'\x1b[C'
        # elif key == 40:
        #     char = b'\x1b[B'
        session.send(key)
    except socket.timeout:
        pass
    print("hmm")
    while True:
        try:
            x = u(session.recv(4096))
            if len(x) == 0:
                print("DONE")
                break
            emit('response', {'data': x})
        except socket.timeout:
            break
    stdout_data = ''.join(map(chr,stdout_data))
    # emit('response', {'data': stdout_data})

# @socketio.on('command')
# def handle_my_custom_event2(resp):
#     stdout_data = []
#     stderr_data = []
#     session = client.open_channel(kind='session')
#     print(resp)
#     session.exec_command(resp['command'])
#     while True:
#         if session.recv_ready():
#             stdout_data += session.recv(4096)
#         if session.recv_stderr_ready():
#             stderr_data += session.recv_stderr(4096)
#         if session.exit_status_ready():
#             break
#     stdout_data = ''.join(map(chr,stdout_data))
#     print(stdout_data)
#     emit('response', {'data': stdout_data})

@socketio.on('login')
def ssh_login(info):
    print(info)
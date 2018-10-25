from flask import Flask, render_template
from flask_socketio import SocketIO
import paramiko

socketio = SocketIO()
hostname = ""
username = ""
password = ""
client = paramiko.Transport((hostname, 22))
client.connect(username=username, password=password)
session = client.open_channel(kind='session')
session.get_pty()
session.invoke_shell()
session.settimeout(0.01)

def create_app():
    app = Flask(__name__, template_folder="views/templates", static_url_path='/static')
    app.secret_key = '5r&6*$PRrdORLy4%Bg3^'

    # Register all views after here
    # =======================
    from ssh_client.views import ssh_client
    

    
    

    app.register_blueprint(ssh_client.page, url_prefix='/')
    socketio.init_app(app)
    return app
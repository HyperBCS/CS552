from flask import Flask, render_template

APP = Flask(__name__, template_folder="views/templates", static_url_path='/static')
APP.secret_key = '5r&6*$PRrdORLy4%Bg3^'


# Register all views after here
# =======================
from ssh_client.views import ssh_client


APP.register_blueprint(ssh_client.page, url_prefix='/')

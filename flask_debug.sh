python3 -c 'import os, subprocess; os.environ["FLASK_APP"]="client.py"; os.environ["FLASK_DEBUG"]="1"; subprocess.Popen(["python3 -m flask run --host=0.0.0.0"], shell=True).wait()'

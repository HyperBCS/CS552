python -c "import os, subprocess; os.environ['FLASK_APP']='client.py'; os.environ['FLASK_DEBUG']='1'; subprocess.Popen('python -m flask run --host=0.0.0.0', shell=True).wait()"

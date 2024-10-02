import subprocess


subprocess.run(["python", "manage.py", "migrate"])
subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])
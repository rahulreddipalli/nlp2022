import os
import subprocess

#subprocess.Popen("pip install --upgrade  --user pip", shell=True)
#subprocess.Popen("pip install -r requirements.txt", shell=True)

print("Starting DearBot")

subprocess.Popen("python dear_bot.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
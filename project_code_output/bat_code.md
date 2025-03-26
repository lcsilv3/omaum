# Código da Funcionalidade: bat
*Gerado automaticamente*



## bat\run_omaum.py

python
import os
import sys
import subprocess
import webbrowser
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    return process.returncode, output, error

def activate_venv():
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        if os.path.exists(activate_script):
            return f"call {activate_script} &&"
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        if os.path.exists(activate_script):
            return f"source {activate_script} &&"
    return ""

def main():
    # Change to the directory containing manage.py
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Activate virtual environment if it exists
    activate_cmd = activate_venv()

    # Start Django server
    command = f"{activate_cmd} python manage.py runserver"
    returncode, output, error = run_command(command)

    if returncode != 0:
        print("An error occurred while running the server:")
        print(error)
        input("Press Enter to exit...")
        return

    # Open web browser
    webbrowser.open("http://127.0.0.1:8000/")

    print("Server is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")

if __name__ == "__main__":
    main()




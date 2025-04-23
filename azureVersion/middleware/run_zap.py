import subprocess
import os

def startzap():
    print (os.getcwd())
    command = [
        "docker", "run",
        "-v", f"{os.getcwd() + '/azureVersion/output'}:/zap/wrk/:rw",
        "-t", "zaproxy/zap-stable",
        "zap.sh", "-cmd", "-autorun", "/zap/wrk/updated_zap.yaml"
    ]

    try:
        result = subprocess.run(command, text=True, capture_output=True)
        print(result.stdout)
        print("Command executed successfully!")
    except subprocess.CalledProcessError as e:
        print("Error occurred while running the command:")
        print(e.stderr)
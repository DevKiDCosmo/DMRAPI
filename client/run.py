import os
import subprocess
import threading

def shell(cmd):
    subprocess.run(cmd, shell=True)

def run():
    # Create 2 Shell Processes and run them in parallel

    client_auth_key = "python main.py"
    client_rest_api = "cd api & uvicorn api.main:app --reload --port 5195"

    thread1 = threading.Thread(target=shell, args=(client_auth_key,))
    thread2 = threading.Thread(target=shell, args=(client_rest_api,))

    # Starten Sie die Threads
    thread1.start()
    thread2.start()

    # Warten Sie, bis beide Threads beendet sind
    thread1.join()
    thread2.join()
                                

if __name__ == "__main__":
    run()
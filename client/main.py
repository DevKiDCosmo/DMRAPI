import base64
from hashlib import sha256
import socket
import os

def create_socket_and_wait_for_ping(port):
    # Erstellen Sie einen TCP/IP-Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binden Sie den Socket an den Port
    server_address = ('127.0.0.1', port)
    sock.bind(server_address)

    # Hören Sie auf eingehende Verbindungen
    sock.listen(1)

    while True:
        # Warten Sie auf eine Verbindung
        print('Warten auf eine Verbindung')
        connection, client_address = sock.accept()

        try:
            print('Verbindung von', client_address)

            # Empfangen Sie die Daten in kleinen Blöcken und senden Sie sie zurück
            while True:
                data = connection.recv(16 * 4)
                print('{!r}'.format(data))

                if data != b"\n":
                    if os.path.isfile('key'):
                        with open("key", "r") as file:
                            if data.decode("utf-8") != file.read():
                                print("NoAuth")
                                status = b"Connection denied. NoAuth"
                                connection.sendall(status)
                                break

                    with open("key", "w") as file:
                        file.write(data.decode("utf-8"))

                    with open("key_instruction", "w") as file:
                        file.write(sha256(base64.b64encode(os.urandom(16) + data).decode("utf-8").encode('utf-8')).hexdigest())
                        
                        status = b"OK"
                        connection.sendall(status)
                
                if data == b"\n":
                    print('Keine Daten mehr von', client_address)
                    break


        finally:
            # Reinigen Sie die Verbindung
            connection.close()

create_socket_and_wait_for_ping(4387)
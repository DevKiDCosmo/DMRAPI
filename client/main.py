import socket

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
                data = connection.recv(16)
                print('Empfangen {!r}'.format(data))
                if data:
                    print('Senden von Daten zurück zum Client')
                    connection.sendall(data)
                else:
                    print('Keine weiteren Daten von', client_address)
                    break
                
        finally:
            # Reinigen Sie die Verbindung
            connection.close()

create_socket_and_wait_for_ping(4387)
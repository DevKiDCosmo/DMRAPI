import base64
import os
import asyncio
import socket

from hashlib import sha256

class cda:
    def ping_device(ip_address):
        response = os.system("ping -c 1 " + ip_address)
        
        if response == 0:
            print(ip_address, 'is up!')
            return True
        else:
            print(ip_address, 'is down!')
            return False

    def generate_key(ip):
        # Generate a key for the device
        return sha256(base64.b64encode(os.urandom(16) + ip.encode()).decode("utf-8").encode('utf-8')).hexdigest()
    
    async def send_key(ip, port, key):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((ip, port))

            s.sendall(key.encode())
            s.sendall(b"\n")

            data = s.recv(1024)

            s.close()

            print('Received', repr(data))

            if data == b"OK":
                return True
            elif data == b"NoAuth":
                return False #[False, "NoAuth"]
            else:
                return False
        except:
            return False

    async def v(ip, key):
        if await cda.send_key(ip, 4387, key): 
            return [True, key, "Has MREC Installed"] # Multi Remote Express Control
        elif await cda.send_key(ip, 4388, key):
            return [True, key, "Has MREC2.0 Installed"]
        elif await cda.send_key(ip, 12953, key):
            return [True, key, "Has AADB Installed"] # Advance ADB
        elif await cda.send_key(ip, 12954, key):
            return [True, key, "Has AADB2.0 Installed"]
        elif await cda.send_key(ip, 64283, key):
            return [True, key, "Has AEXp Installed"] # Advance Express
        elif await cda.send_key(ip, 51985, key):
            return [True, key, "Has ADBEx Installed"] # ADB Express
        else:
            return [False, key, "No Installtion is found by the given key or the auth was denied."]

    def v_(ip, key):
        return [True, key, "Has MREC Installed"]

    async def check_device_alive(self, ip):

        # Add a check if the device is alive without any installment
        cda.ping_device(ip)
                
        key = cda.generate_key(ip)
        print(key)

        # Check if a MREC is installed on port 4387
        return await cda.v(ip, key)
        # Else break and send an error

    async def check_device_alive_key(self, ip, key):
        cda.ping_device(ip)
        return await cda.v(ip, key)
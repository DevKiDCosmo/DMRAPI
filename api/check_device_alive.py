import base64
import os
import asyncio
import websockets

from hashlib import sha256

class cda:
    def ping_device(ip_address):
        response = os.system("ping -c 1 " + ip_address)
        
        if response == 0:
            print(ip_address, 'is up!')
        else:
            print(ip_address, 'is down!')

    def generate_key(ip):
        # Generate a key for the device
        return sha256(base64.b64encode(os.urandom(16) + ip.encode()).decode("utf-8").encode('utf-8')).hexdigest()
    
    async def send_key(ip, port, key):
        uri = f"ws://{ip}:{port}"
        async with websockets.connect(uri) as websocket:
            await websocket.send(key)
            response = await websocket.recv()
            print(f"Received: {response}")
            if response == "OK":
                print("Device is alive")
                return True
            else:
                print("Device is not alive")
                return False

    def v_(ip, key):
        if asyncio.get_event_loop().run_until_complete(cda.send_key(ip, 4387, key)): 
            return [True, key, "Has MREC Installed"] # Multi Remote Express Control
        elif asyncio.get_event_loop().run_until_complete(cda.send_key(ip, 4388, key)):
            return [True, key, "Has MREC2.0 Installed"]
        elif asyncio.get_event_loop().run_until_complete(cda.send_key(ip, 12953, key)):
            return [True, key, "Has AADB Installed"] # Advance ADB
        elif asyncio.get_event_loop().run_until_complete(cda.send_key(ip, 12954, key)):
            return [True, key, "Has AADB2.0 Installed"]
        elif asyncio.get_event_loop().run_until_complete(cda.send_key(ip, 64283, key)):
            return [True, key, "Has AEXp Installed"] # Advance Express
        elif asyncio.get_event_loop().run_until_complete(cda.send_key(ip, 51985, key)):
            return [True, key, "Has ADBEx Installed"] # ADB Express
        else:
            return [False, key, "No MREC etc. Installed"]

    def v(ip, key):
        return [True, key, "Has MREC Installed"]

    def check_device_alive(self, ip):

        cda.ping_device(ip)
        key = cda.generate_key(ip)
        print(key)

        # Check if a MREC is installed on port 4387
        return cda.v(ip, key)
        # Else break and send an error

    def check_device_alive_key(self, ip, key):
        cda.ping_device(ip)
        return cda.v(ip, key)
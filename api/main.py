from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from check_device_alive import *

import pandas as pd

app = FastAPI()

# At the boot, check if all the device are alive, else delete them. Later in the config file, we can add a flag to disable this feature


def get_device():
    try:
        return pd.read_csv("device.csv").values.tolist()
    except:
        return []
    

device = get_device()

def timestamp():
    return pd.Timestamp.now()

@app.patch("/device/")
def update_device():
    global device
    device = get_device()
    return {"msg": "Devices updated", "status": "success"}

@app.post("/device/{key}")
def is_exist(key: str):
    # Get IP
    ip = None
    for d in device:
        if d[2] == key:
            ip = d[1]

    cda_instance = cda()
    st = cda_instance.check_device_alive_key(ip=ip, key=key)

    return {"msg": "Device is alive", "device_id": d[0], "ip": d[1], "key": d[2], "timestamp": d[3], "Status": st}

@app.get("/")
def read_root():
    return {"msg": "Welcome to the DMR API", "status": "success", "ver": "1.0beta"}

@app.get("/device/")
def send_device():
    return device

def save_device():
    df = pd.DataFrame(device, columns=["device_id", "ip", "key", "timestamp"])
    df.to_csv("device.csv", index=False)

def get_index(device_id: int):
    for i, d in enumerate(device):
        if d[0] == device_id:
            return i
    return None

def exist_element(device_id: int, t: int = 0):
    for d in device:
        if d[t] == device_id:
            return True
    return False

@app.put("/device/{device_id}/{ip}")
async def add_device(device_id: int, ip: str):
    if exist_element(device_id):
        return {"msg": "Device already exists", "device_id": device_id}
    
    if exist_element(ip, t=1):
        return {"msg": "IP already exists", "ip": ip}

    cda_instance = cda()
    st = await cda_instance.check_device_alive(ip=ip)

    if (st[0] == False):
        return {"msg": "Device is not alive", "device_id": device_id, "ip": ip}

    device.append((device_id, ip, st[1], timestamp()))
    save_device()
    return {"id": device_id, "ip": ip, "key": st[1], "timestamp": timestamp()}

@app.get("/devicekey/{ip}")
def get_device_key(ip: str):
    return cda.generate_key(ip)

@app.put("/devicekey/{device_id}/{ip}/{key}")
async def add_device_key(device_id: int, ip: str, key: str):
    if exist_element(device_id):
        return {"msg": "Device already exists", "device_id": device_id}
    
    if exist_element(ip, t=1):
        return {"msg": "IP already exists", "ip": ip}

    cda_instance = cda()
    st = await cda_instance.check_device_alive_key(ip, key)

    if (st[0] == False):
        return {"msg": "Device is not alive", "device_id": device_id, "ip": ip}

    device.append((device_id, ip, key, timestamp()))
    save_device()
    return {"id": device_id, "ip": ip, "key": key, "timestamp": timestamp()}

@app.get("/key/{key}")
def get_key(key: str):
    for d in device:
        if d[2] == key:
            return {"device_id": d[0], "ip": d[1], "key": d[2], "timestamp": d[3]}
    return {"msg": "Key not found", "key": key ,"timestamp": timestamp()}

@app.delete("/device/{device_id}")
def delete_device(device_id: int):
    if exist_element(device_id):
        device.pop(get_index(device_id))
        save_device()
        return {"msg": "Device deleted", "device_id": device_id}
    return {"msg": "Device not found", "device_id": device_id}

@app.delete("/devicekey/{key}")
def delete_device_key(key: str):
    for d in device:
        if d[2] == key:
            device.pop(get_index(d[0]))
            save_device()
            return {"msg": "Device deleted", "device_id": d[0]}
    return {"msg": "Device not found", "key": key}

@app.post("/reset/device")
def reset_device():
    # Delete file
    try:
        os.remove("device.csv")
    except:
        return {"msg": "Device reset failed", "status": "failed"}

    global device
    device = get_device()

    return {"msg": "Device reset", "status": "success"}

@app.get("/key_login/{key}")
async def key_login(key: str):
    for d in device:
        if d[2] == key:
            cda_instance = cda()
            st = await cda_instance.check_device_alive_key(ip=d[1], key=d[2])

            return {"msg": "Login success", "device_id": d[0], "ip": d[1], "key": d[2], "timestamp": d[3], "Status": st}
    return {"msg": "Key not found", "key": key ,"timestamp": timestamp()}

@app.get("/device_login/{device_id}")
async def log_device(device_id: int):
    for d in device:
        if d[0] == device_id:
            cda_instance = cda()
            st = await cda_instance.check_device_alive_key(ip=d[1], key=d[2])

            return {"msg": "Login success", "device_id": d[0], "ip": d[1], "key": d[2], "timestamp": d[3], "Status": st}
    return {"msg": "Device not found", "device_id": device_id}

@app.get("/device_ip/{ip}")
async def log_device_ip(ip: str):
    for d in device:
        if d[1] == ip:
            cda_instance = cda()
            st = await cda_instance.check_device_alive_key(ip=d[1], key=d[2])

            return {"msg": "Login success", "device_id": d[0], "ip": d[1], "key": d[2], "timestamp": d[3], "Status": st}
    return {"msg": "Device not found", "ip": ip}
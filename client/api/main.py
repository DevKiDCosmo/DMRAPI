from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import os

from hashlib import sha256

app = FastAPI()

key = ""

if os.path.isfile("key"):
    with open("key", "r") as file:
        key = file.read()
else:
    exit("Key file not found")

@app.get("/")
def read_root():
    return {"msg": "Welcome to the DMR API", "status": "success", "ver": "1.0beta", "keySHA": sha256(key.encode()).hexdigest()}

@app.get("/api/login/{key_}")
def login(key_: str):
    if key == key_:
        # Create session

        return {"msg": "Login successful", "status": "success"}
    else:
        return {"msg": "Login failed", "status": "failed"}

@app.get("/device/key/")
def Instruction_Key_Device():
    with open("key_instruction", "r") as file:
        key_instruction = file.read()
    return {"port": 4522, "key_instruction": key_instruction}

# Change key

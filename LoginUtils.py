import hashlib
import uuid
import requests


def get_machine_id():
    mac = uuid.getnode()
    print(f"MID: {hashlib.sha256(str(mac).encode('utf-8')).hexdigest()}")
    return hashlib.sha256(str(mac).encode('utf-8')).hexdigest()


def apiVerify(key):
    req = requests.post("https://cloakapi.herokuapp.com/license/verify",
                        json={"license_key": key, "machine_id": get_machine_id()})
    print(f"printing the req from login utils {req.text}")
    return req.json()


def apiActivate(key):
    req = requests.post("https://cloakapi.herokuapp.com/license/activate",
                        json={"license_key": key, "machine_id": get_machine_id()})
    print(f"printing the req from login utils {req}")
    return req.json()


if __name__ == '__main__':
    pass

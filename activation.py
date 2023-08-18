import os
import sys
from App import App
from Login import LoginWindow
from LoginUtils import apiVerify

if __name__ == '__main__':
    print(os.getcwd())
    if getattr(sys, 'frozen', False):
        Current_Path = os.path.dirname(sys.executable)
    else:
        Current_Path = str(os.path.dirname(__file__))

    print(f"Current Path fix attempt: {Current_Path}")

    if not os.path.exists(f"{Current_Path}/Info"):
        os.mkdir(f"{Current_Path}/Info")
        with open(f"{Current_Path}/Info/key.txt", 'w') as f:
            pass

    try:
        if not os.path.getsize(f"{Current_Path}/Info/key.txt") > 0:
            print("FIRST TIME RUNNING, OR key.txt is empty.")
            login = LoginWindow(Current_Path)
            login.add_frame()
        else:
            with open(f"{Current_Path}/Info/key.txt", 'r') as f:
                key = f.readline().strip()
                print(key)
                response = apiVerify(key)
                print(response)
            try:
                print(response["detail"][0]['msg'])
                status = response["detail"][0]['msg']
            except KeyError:
                print(response['status'])
                status = response['status']

            if status == "VERIFIED":
                app = App()
            else:
                app = LoginWindow(Current_Path)
                app.add_frame()

    except FileNotFoundError:
        print(f"FILE NOT FOUND, make sure you have a folder called {os.getcwd()}/CloakAI at this path")


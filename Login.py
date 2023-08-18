import os
import sys
from tkinter import *
from tkinter import messagebox
from LoginUtils import apiActivate
from App import App


class LoginWindow:

    def __init__(self, CurrentPath=None):
        self.CurrentPath = CurrentPath
        self.win = Tk()
        self.win.iconbitmap(self.resource_path("icon.ico"))
        # reset the window and background color
        self.canvas = Canvas(self.win, width=600, height=500, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x525"
        print(str1)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("Cloak.AI | PRODUCT REGISTRATION")

    def writeKeyFile(self, regKey, user, password):
        if self.CurrentPath:
            print("attempting to write reg key after successful registration because there wasn't one, or it was incorrect")
            with open(f"{self.CurrentPath}/Info/key.txt", 'w') as f:
                f.write(f"{regKey}\n")
                f.write(f"{user}\n")
                f.write(f"{password}")

    def add_frame(self):
        self.frame = Frame(self.win, height=450, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        self.img = PhotoImage(file=self.resource_path('login.png'))
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x + 80, y=y + 0)

        # now create a login form
        self.label = Label(self.frame, text="Registration ")
        self.label.config(font=("Arial", 20, 'bold'), fg="#235474")
        self.label.place(x=213 - x, y=y + 170)

        self.pslabel = Label(self.frame, text="License Key")
        self.pslabel.config(font=("Arial", 12, 'bold'), fg="#58a884")
        self.pslabel.place(x=25, y=y + 260)

        self.keybox = Entry(self.frame, show='*', font='Courier 12')
        self.keybox.place(x=130, y=y + 260)
        self.keybox.bind("<Control-a>", lambda event: self.select_all(1))

        self.pslabel2 = Label(self.frame, text="Rewrite User")
        self.pslabel2.config(font=("Arial", 12, 'bold'), fg="#58a884")
        self.pslabel2.place(x=25, y=y + 290)

        self.keybox2 = Entry(self.frame, font='Courier 12')
        self.keybox2.place(x=130, y=y + 290)
        self.keybox2.bind("<Control-a>", lambda event: self.select_all(2))

        self.pslabel3 = Label(self.frame, text="Password")
        self.pslabel3.config(font=("Arial", 12, 'bold'), fg="#58a884")
        self.pslabel3.place(x=25, y=y + 320)

        self.keybox3 = Entry(self.frame, font='Courier 12')
        self.keybox3.place(x=130, y=y + 320)
        self.keybox3.bind("<Control-a>", lambda event: self.select_all(3))

        self.button = Button(self.frame, text="Register", font='Arial 15 bold', command=self.postAPI)
        self.button.place(x=170, y=y + 350)

        self.win.mainloop()

    def select_all(self,box_id):
        print(box_id)
        # print("selecting all")
        if box_id == 1:
            self.keybox.select_range(0, 'end')
            self.keybox.icursor('end')
        elif box_id == 2:
            self.keybox2.select_range(0, 'end')
            self.keybox2.icursor('end')
        elif box_id == 3:
            self.keybox3.select_range(0, 'end')
            self.keybox3.icursor('end')
        return 'break'

    def postAPI(self):

        key = self.keybox.get()
        rewriteruser = self.keybox2.get()
        rewriterpassword = self.keybox3.get()
        response = apiActivate(key.strip())
        try:
            print(response["detail"][0]['msg'])
            status = response["detail"][0]['msg']
        except KeyError:
            print(response['status'])
            status = response['status']

        if status == "ACTIVATED":
            messagebox.showinfo("Activation Successful",
                                message="Thank you for purchasing Cloak.AI. Your key has been activated and is now tied to this computer. The app will not work on any other machine.\n\nKey Status: Lifetime")
            self.writeKeyFile(key, rewriteruser, rewriterpassword)
            self.win.destroy()
            app = App()

        else:
            messagebox.showerror("Activation Error",
                                 message="This key is invalid. Please make sure you have pasted it correctly, with no trailing spaces.")
            messagebox.showinfo("Tip",
                                message="If you have activated your license, but you are being prompted to register, it means your key is incorect in the key.txt file.")

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    pass

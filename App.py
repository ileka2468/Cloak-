import datetime
import os
import platform
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from tkinter import *
from tkinter import messagebox, ttk
import tkmacosx as mtk

from driver import RewriteAutomate, parseFile
class App:
    def __init__(self):
        self.win = Tk()
        self.win.iconbitmap(self.resource_path('icon.ico'))
        self.N = 0
        self.textList = []
        self.init(self.win)

    def init(self, win):
        if self.osIs() == "Mac":
            win.geometry('500x740')
        else:
            win.geometry('500x930')
        win.title('CloakAI')
        self.layout(win)
        win.mainloop()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    def layout(self, win):
        self.mainFrame = Frame(win)
        self.mainFrame.pack(expand=True, fill="both")
        Title = Label(self.mainFrame, text='CloakAI', font=('Arial', 25, 'bold'), fg='#26b379')
        Title.pack(pady=10)

        self.list_box = Listbox(self.mainFrame, height=20, width=40, bg="white", activestyle='dotbox',
                                font=('Arial', 15),
                                fg="black")
        self.list_box.pack()

        if self.osIs() == "Mac":
            bind = "Command-a"
        else:
            bind = "<Control-a>"

        self.entryBox = Text(self.mainFrame, font=('Arial', 14), height=10, width=43)
        self.entryBox.bind(bind, self.select_all)
        self.entryBox.pack(pady=20)

        buttonBay = Frame(self.mainFrame)
        buttonBay.pack()

        gridFrame = Frame(buttonBay)
        gridFrame.grid(row=0, column=0)

        currOs = self.osIs()

        if currOs == "Mac":
            add = mtk.Button(gridFrame, text="Add", bg='#7a3ee0', fg='white', command=self.addToList)
            clear = mtk.Button(gridFrame, text="Clear", bg='#7a3ee0', fg='white', command=self.clear)
            delete = mtk.Button(gridFrame, text="delete selection", bg='#7a3ee0', fg='white', command=self.deleteSelection)
            start = mtk.Button(self.mainFrame, text='Start Automation', command=self.startAutomationThread,
                               bg='#58a884',
                               fg='white',
                               height=30)


        else:
            add = Button(gridFrame, text="Add", bg='#235474', fg='white', command=self.addToList)
            clear = Button(gridFrame, text="Clear", bg='#235474', fg='white', command=self.clear)
            delete = Button(gridFrame, text="delete selection", bg='#235474', fg='white', command=self.deleteSelection)
            start = Button(self.mainFrame, text='Start Automation', command=self.startAutomationThread,
                               bg='#58a884',
                               fg='white',
                               height=2)


        add.grid(row=0, column=0, padx=5)
        clear.grid(row=0, column=1)
        delete.grid(row=0, column=2)

        start.pack(pady=10)

        self.progress = ttk.Progressbar(self.mainFrame, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)

    def select_all(self, event):
        print("selecting all")
        self.entryBox.tag_add(SEL, "1.0", END)
        self.entryBox.mark_set(INSERT, END)
        self.entryBox.see(INSERT)
        return 'break'

    def addToList(self):
        text = self.entryBox.get('1.0', END).strip()
        if len(text) != 0:
            self.N += 1
            self.entryBox.delete('1.0', END)
            self.list_box.insert(self.N, text.strip())
            self.textList.append(text)
            print(f"Current list: {self.textList}")

    def clear(self):
        self.entryBox.delete('1.0', END)

    def deleteSelection(self):
        selection = self.list_box.curselection()
        if selection:
            index = selection[0]
            value = self.list_box.get(index)
            self.list_box.delete(index)
            del self.textList[index]
            self.N -= 1
            print(f"removed {value} from list.")
            print(f"Updated list: {self.textList}")

    def startAutomationThread(self):
        automation_thread = threading.Thread(target=self.startAutomation)
        automation_thread.start()

    def startAutomation(self):
        results = []
        if len(self.textList) == 0:
            messagebox.showwarning("No Text Added", "You must have at least one entry.")
        else:
            for entry in self.textList:
                if not entry.count(" ") >= 9:
                    results.append(False)

            if all(results):

                if len(self.textList) > 0:
                    devMode = False
                    if self.osIs() == 'Mac':
                        script_dir = os.getcwd()
                        self.output_dir = os.path.join(script_dir, 'Desktop/AutomatorOutput')
                        print(self.output_dir)
                    else:

                        script_dir = os.getcwd()
                        self.output_dir = os.path.join(script_dir, 'CloakAIOutput')
                        print(self.output_dir)

                    if devMode:
                        self.output_dir = f"{script_dir}/DebugOutput"
                        if not os.path.exists(self.output_dir):
                            os.mkdir(self.output_dir)
                    else:
                        if not os.path.exists(self.output_dir):
                            os.mkdir(self.output_dir)

                    now = datetime.datetime.now()
                    output_file_name = "output_{:%Y-%m-%d_%H-%M-%S}.txt".format(now)

                    finalOutPutPath = f"{self.output_dir}/{output_file_name}"

                    automator = RewriteAutomate(finalOutPutPath)

                    print("Rewrite started")
                    inputs = parseFile(self.textList)
                    num_tasks = len(inputs)

                    # Set the progress bar maximum value and initial value
                    self.progress["maximum"] = num_tasks
                    self.progress["value"] = 0

                    with ThreadPoolExecutor(max_workers=3) as executor:
                        for i, input in enumerate(inputs):
                            instance = RewriteAutomate(finalOutPutPath)
                            driver = instance.login()
                            print(f"Starting task {i} on thread {threading.current_thread().name}")
                            future = executor.submit(instance.start, [input], driver)

                            # Update the progress bar value
                            def update_progress_bar(future):
                                self.progress["value"] += 1
                                self.win.update_idletasks()

                            future.add_done_callback(update_progress_bar)
            else:
                messagebox.showwarning("One or more entries is too short",
                                       "Each entry must be greater than or equal to 10 words.")

    def osIs(self):
        if platform.system() == "Darwin":
            return "Mac"
        elif platform.system() == "Linux":
            return "Linux"
        elif platform.system() == "Windows":
            return "Windows"


if __name__ == '__main__':
    pass

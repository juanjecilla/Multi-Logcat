from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox

from adb_tools.adb_manager import AdbManager


class Application(Frame):

    def __init__(self, master=None, cnf=None, num_devices=0, **kw):
        super().__init__(master, cnf, **kw)
        if cnf is None:
            cnf = {}
        self.logcats = []
        self.max_width = master.winfo_screenwidth()
        self.max_height = master.winfo_screenheight()
        self.master = master
        self.num_devices = num_devices
        self.adb_manager = AdbManager()
        # self.adb_manager.start()
        # print(num_devices)

        device = self.adb_manager.get_current_devices()[0]

        master.geometry("{}x{}".format(self.max_width, self.max_height))

        devices_button = Button(text="Devices", command=self.add_horizontal_view)
        devices_button.grid(row=0, column=0)

        stop_button = Button(text="Stop", command=self.stop)
        stop_button.grid(row=0, column=1)

        app_list_combo = Combobox()
        app_list_combo.grid(row=0, column=2)
        app_list_combo["values"] = self.adb_manager.get_installed_packages(device)

        self.logcat_group = Frame(master, padx=5, pady=5, background='black')
        self.master.configure(background='black')
        self.logcat_group.grid(row=1, column=0, padx=10, pady=10, sticky=E + W + N + S)

        for i in range(self.num_devices):
            txtbox = scrolledtext.ScrolledText(self.logcat_group)
            txtbox.grid(row=i, column=0, sticky=E + W + N + S)

            self.logcat_group.rowconfigure(i, weight=1)
            self.logcat_group.columnconfigure(0, weight=1)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)



    def add_horizontal_view(self):
        num_children = len(self.logcat_group.children)

        txtbox = scrolledtext.ScrolledText(self.logcat_group)
        txtbox.grid(row=num_children, column=0, sticky=E + W + N + S)
        txtbox.configure(background='#1b1b1b')
        txtbox.tag_config('DEBUG', foreground='#56bb00')
        txtbox.tag_config('INFO', foreground='#00b6bb')
        txtbox.tag_config('WARNING', foreground='#bbac00')
        txtbox.tag_config('ERROR', foreground='#ff6b68')
        txtbox.tag_config('DEFAULT', foreground='white')

        self.logcat_group.rowconfigure(num_children, weight=1)
        self.logcat_group.columnconfigure(0, weight=1)

        device = self.adb_manager.get_current_devices()[0]
        self.adb_manager.get_logcat(device, callback=self.add_line)

    def stop(self):
        self.adb_manager.stop_logcat(0)

    def add_text(self, data):
        text = self.logcat_group.children.get('!frame').children.get('!scrolledtext')

        for item in data:
            text.insert(END, item["text"], item["type"])
            text.see("end")

    def add_line(self, data):
        text = self.logcat_group.children.get('!frame').children.get('!scrolledtext')

        text.insert(END, data["text"], data["type"])
        text.see("end")

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from Code.log_page import LoginPage


class InitialPage:
    Images = r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images"

    def __init__(self, root):
        self.root = root
        self.root.title("PriorNet-Welcome")
        x = self.root.master.winfo_x()
        y = self.root.master.winfo_y()
        self.root.geometry("400x340+%d+%d" % (x, y))

        log_img = Image.open(os.path.join(self.Images, "login.png"))
        signup_img = Image.open(os.path.join(self.Images, "signup.png"))
        logo_img = Image.open(os.path.join(self.Images, "logo_2.png"))
        go_back_img = Image.open(os.path.join(self.Images, "arrow-back-icon.png"))

        log_img = log_img.resize((200, 80))
        signup_img = signup_img.resize((200, 80))
        logo_img = logo_img.resize((400, 100))
        go_back_img = go_back_img.resize((30, 30))

        log_img = ImageTk.PhotoImage(log_img)
        signup_img = ImageTk.PhotoImage(signup_img)
        logo_img = ImageTk.PhotoImage(logo_img)
        go_back_img = ImageTk.PhotoImage(go_back_img)

        self.logo_lbl = tk.Label(self.root, image=logo_img)
        self.logo_lbl.pack(side=tk.TOP)

        self.login_btn = tk.Button(self.root, image=log_img, border=0, borderwidth=0,
                                   command=lambda: self.log_page(LoginPage, "in"))
        self.login_btn.pack(pady=10)

        self.signup_btn = tk.Button(self.root, image=signup_img, borderwidth=0,
                                    command=lambda: self.log_page(LoginPage, "up"))
        self.signup_btn.pack(pady=(5, 10))

        self.go_back_btn = tk.Button(self.root, image=go_back_img, borderwidth=0, command=self.back)
        self.go_back_btn.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

        self.root.mainloop()

    def back(self):
        self.root.withdraw()
        self.root.master.deiconify()

    def exit_app(self):
        msg_box = messagebox.askquestion("Exit", "Are you sure you want to exit?", icon='warning')
        if msg_box == "yes":
            self.root.destroy()

    def log_page(self, win_class, go):
        self.root.withdraw()
        if go == "in":
            win1 = tk.Toplevel(self.root)
            win_class(win1, go)
        else:
            win2 = tk.Toplevel(self.root)
            win_class(win2, go)

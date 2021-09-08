import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import socket
from Code.initial_page import InitialPage
from Code.chat_box import ChatBox

# GLOBAL CONSTANT
HEADER = 10
IP = "localhost"
PORT = 12345


class StartPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PriorNet")
        self.root.configure(bg="#56d1c3")
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_pathname(self.root.winfo_id()))
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            foreground="white",
            background="#3437eb",
            font="Helvetica",
            fontsize=12
        )

        def on_closing():
            msgbox = messagebox.askquestion("Exit", "Are you sure you want to exit?", icon='warning')
            if msgbox == "yes":
                self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        def priornet():
            self.root.withdraw()
            self.init_win = tk.Toplevel(self.root)
            InitialPage(self.init_win )

        img = Image.open(r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images\fin_log.png")
        img = img.resize((200, 50))
        image1 = ImageTk.PhotoImage(img)

        self.priornet_btn = tk.Button(self.root, image=image1, borderwidth=0, command=priornet)
        self.priornet_btn.pack(fill=tk.X, side=tk.LEFT, padx=(20, 10), pady=20)

        def chat_room():
            self.root.withdraw()
            self.chatroom_win = tk.Toplevel(self.root)
            self.chatroom_win.title("ChatRoom")

            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.chatroom_win.geometry("+%d+%d" % (x, y))

            self.nick_lbl = ttk.Label(self.chatroom_win, text="Pick a Nickname:", style="BW.TLabel")
            self.nick_lbl.pack(pady=5)

            self.nick_entry = tk.Entry(self.chatroom_win, font=15)
            self.nick_entry.pack(fill=tk.X, padx=10, pady=5)

            def chat_room():
                if self.nick_entry.get() != "" and len(self.nick_entry.get()) > 3:
                    FLAG = False
                    try:
                        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.client.connect((IP, PORT))
                        self.client.setblocking(False)
                        FLAG = True
                    except:
                        messagebox.showinfo("No server", "Unable to connect with server. Try again later!")
                    if FLAG:
                        self.chatroom_win.withdraw()
                        self.nex_win = tk.Toplevel(self.root)
                        ChatBox(self.client, self.root, self.nex_win, self.nick_entry.get())
                elif self.nick_entry.get() =="":
                    messagebox.showinfo("Provide nickname", "No Nickname Provided")
                else:
                    messagebox.showinfo("Short nickname", "Nickname too short!")

            self.ok_btn = tk.Button(self.chatroom_win, text="Enter ChatRoom", command=chat_room)
            self.ok_btn.pack(pady=5)

            def on_closing():
                self.chatroom_win.withdraw()
                self.root.deiconify()

            self.chatroom_win.protocol("WM_DELETE_WINDOW", on_closing)

            self.chatroom_win.mainloop()

        img2 = Image.open(r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images\chatroom.png")
        img2 = img2.resize((200, 50))
        image2 = ImageTk.PhotoImage(img2)

        self.priornet_public = tk.Button(self.root, image=image2, borderwidth=0, command=chat_room)
        self.priornet_public.pack(side=tk.RIGHT, padx=(10,20), pady=20)

        self.root.mainloop()


StartPage()

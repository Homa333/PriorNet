import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


from Code.news_feed import NewsFeed
from Code.friends import FriendList
from Code.add_friend import AddFriend


class HomePage:

    def __init__(self,root, user_id, user_name, user_port):
        self.images_path = r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images"
        self.user_id = user_id
        self.user_name = user_name

        self.root = root
        self.root.title("PriorNet-Home Page")
        x = self.root.master.winfo_x()
        y = self.root.master.winfo_y()
        self.root.geometry("+%d+%d" % (x, y))

        def quit_homepage():
            msg_box = messagebox.askquestion("Exit", "Are you sure you want to exit?", icon='warning')
            if msg_box == "yes":
                self.root.master.master.master.destroy()

        self.root.protocol("WM_DELETE_WINDOW", quit_homepage)

        tk.Grid.columnconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 1, weight=1)
        # tk.Grid.rowconfigure(self.root, 1, weight=1)

        self.greet_label = tk.Label(self.root, font={"Source Code Pro", 10}, text="Hello " + user_name + ",")
        self.greet_label.grid(column=0, row=1, padx=10, pady=10, sticky="nw")
        try:
            img1 = Image.open(os.path.join(self.images_path, "newsfeed.png"))
            img1 = img1.resize((120, 120))
            self.imag = ImageTk.PhotoImage(img1)
        except Exception as e:
            print(e)


        def news_feed(win_class):
            global win1
            self.root.withdraw()
            win1 = tk.Toplevel(self.root)
            win_class(self.root, win1, self.user_id, self.user_name)

        self.newsfeed_btn = tk.Button(self.root, image=self.imag, borderwidth=0, command=lambda: news_feed(NewsFeed))
        self.newsfeed_btn.grid(column=0, row=2, pady=20, padx=20, sticky="n")

        img3 = Image.open(os.path.join(self.images_path, "friends.png"))
        img3 = img3.resize((120, 120))
        self.img3 = ImageTk.PhotoImage(img3)

        def friend_list(win_class):
            global win2
            self.root.withdraw()
            win2 = tk.Toplevel(self.root)
            win_class(self.root, win2, user_id, user_name, user_port)

        self.friends_btn = tk.Button(self.root, image=self.img3, borderwidth=0,
                                     command=lambda: friend_list(FriendList))
        self.friends_btn.grid(column=1, row=2, pady=20, padx=20, sticky="n")

        img2 = Image.open(os.path.join(self.images_path, "addfriend.png"))
        img2 = img2.resize((100, 100))
        self.image2 = ImageTk.PhotoImage(img2)

        def add_friend():
            self.root.withdraw()
            win = tk.Toplevel(self.root)
            AddFriend(win, user_id, user_name)

        self.add_friend = tk.Button(self.root, image=self.image2, borderwidth=0, command=add_friend)
        self.add_friend.grid(column=0, row=4, pady=20, padx=20, sticky="n")

        img4 = Image.open(os.path.join(self.images_path, "logout.png"))
        img4 = img4.resize((100, 100))
        self.image4 = ImageTk.PhotoImage(img4)

        def logout():
            msg = messagebox.askquestion("Logout", "Are you sure to logout?", icon="warning")
            if msg == "yes":
                self.root.withdraw()
                self.root.master.master.deiconify()

        self.logout = tk.Button(self.root, image=self.image4, borderwidth=0, command=logout)
        self.logout.grid(column=1, row=4, pady=20, padx=20, sticky="n")

        self.root.mainloop()

import functools
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread

from Code.DBMS_Connect import DbmsConnect
from Code.chat_with import ChatWith
from Code.userprofile import UserProfile


class FriendList:
    friends_list = {}

    def __init__(self, master, win, user_id, username, port):
        self.username = username
        self.user_id = user_id
        self.port = port
        self.win = win
        self.win.geometry("300x400")

        def quit_friend_list():
            self.win.withdraw()
            children_widgets = self.win.winfo_children()
            for child_widget in children_widgets:
                if child_widget.winfo_class() == 'Entry':
                    child_widget.delete(0, tk.END)
            master.deiconify()

        self.win.protocol("WM_DELETE_WINDOW", quit_friend_list)

        """Upper segment for Title, search box and search button"""
        self.upper_seg = tk.Frame(self.win)
        self.upper_seg.pack(anchor="w", fill=tk.X)

        self.friend_list_lbl = tk.Label(self.upper_seg, text="Friend List", font=("Calibri", 20), anchor="e")
        self.friend_list_lbl.grid(column=0, row=1, sticky="w", padx=5)

        self.search_entry = tk.Entry(self.upper_seg, font=("Calibri", 12))
        self.search_entry.grid(column=0, row=2, padx=5, pady=5, sticky="ew")

        def search_friends():
            name = self.search_entry.get()
            FLAG = True
            if name != "":
                for friend_id, friend_name, po in self.friends_list.items():
                    if name.lower() == friend_name.lower():
                        for widget in self.scrollable_frame.winfo_children():
                            widget.destroy()
                        FLAG = False
                        searched_friend = ((friend_name, friend_id),)
                        print("in")
                        self.friend_with(searched_friend)
            else:
                messagebox.showwarning("Search", "No username given")
            if FLAG:
                messagebox.showwarning("Search", "Friend not found")

        self.search_button = tk.Button(self.upper_seg, text="Search friends", command=search_friends)
        self.search_button.grid(column=1, row=2, padx=5, pady=5, sticky="w")

        """Separator to separate Upper segment and lower segment"""
        self.separator = ttk.Separator(self.win, orient=tk.HORIZONTAL)
        self.separator.pack(fill=tk.X, padx=10)

        # Segment to show Friends list
        self.lower_seg = tk.Frame(self.win)
        self.lower_seg.pack(fill=tk.X)
        tk.Grid.columnconfigure(self.lower_seg, 0, weight=1)
        tk.Grid.columnconfigure(self.lower_seg, 1, weight=1)
        tk.Grid.columnconfigure(self.lower_seg, 2, weight=1)

        self.display_friends = tk.Canvas(self.lower_seg)
        self.display_friends.pack(side="left", fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.lower_seg, orient="vertical", command=self.display_friends.yview)
        self.scrollbar.pack(side="right", fill=tk.Y)

        self.scrollable_frame = ttk.Frame(self.display_friends)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.display_friends.configure(
                scrollregion=self.display_friends.bbox("all")
            )
        )
        self.display_friends.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.display_friends.configure(yscrollcommand=self.scrollbar.set)

        self.friends_details = DbmsConnect('priornet')
        self.friends_details.get_data_from_database(f"select username, user_id, port_number from user where user_id "
                                                    f"in (select "
                                                    f" FriendIDs from friends where UID = '{self.user_id}'or FriendIDs"
                                                    f"='{self.user_id}') or user_id in (select UID from friends"
                                                    f" where UID = '{self.user_id}'or FriendIDs='{self.user_id}')")

        self.friend_with(self.friends_details.data)

        self.win.mainloop()

    def friend_with(self, friend_list):
        friend_count = 0
        row = 0

        def profile(idx):

            UserProfile(self.win, friend_list[idx][0], friend_list[idx][1])

        def chat(idx):
            friend_name = friend_list[idx][0]
            friend_port = friend_list[idx][2]
            ChatWith(self.username, self.port, friend_name, friend_port)

        for name, id, port in friend_list:
            frnd_name = ''.join(name)
            if frnd_name != self.username:
                self.friends_list[''.join(id)] = frnd_name

                self.frnd_name_lbl = tk.Label(self.scrollable_frame, text=frnd_name)
                self.frnd_name_lbl.grid(row=row, column=0, padx=(10, 100))

                self.profile_btn = tk.Button(self.scrollable_frame, text="See Profile",
                                             command=functools.partial(profile, idx=friend_count))
                self.profile_btn.grid(row=row, column=1, padx=5)

                self.chat_btn = tk.Button(self.scrollable_frame, text="Chat", command=functools.partial(chat,
                                                                                                        idx=friend_count))
                self.chat_btn.grid(row=row, column=2, padx=5)

                self.separator = ttk.Separator(self.scrollable_frame, orient=tk.HORIZONTAL)
                self.separator.grid(row=row + 1, column=0, columnspan=4, padx=(5, 0), pady=5, sticky="ew")
                row += 2
            friend_count += 1

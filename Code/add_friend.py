import tkinter as tk
from tkinter import messagebox, ttk
import functools
import mysql.connector.errors

from Code.DBMS_Connect import DbmsConnect
from Code.userprofile import UserProfile


class AddFriend:
    user_list = {}

    def __init__(self, win, user_id, username):
        self.username = username
        self.user_id = user_id
        self.root = win

        def quit_add_friend():
            self.root.withdraw()
            children_widgets = self.root.winfo_children()
            for child_widget in children_widgets:
                if child_widget.winfo_class() == 'Entry':
                    child_widget.delete(0, tk.END)
            self.root.master.deiconify()

        self.root.protocol("WM_DELETE_WINDOW", quit_add_friend)

        self.upper_seg = tk.Frame(self.root)
        self.upper_seg.pack(anchor="w", fill=tk.X)

        self.friend_list_lbl = tk.Label(self.upper_seg, text="User list", font=("Calibri", 20), anchor="e")
        self.friend_list_lbl.grid(column=0, row=1, sticky="w", padx=5)

        def received_requests():
            self.root.withdraw()
            display_received_req = tk.Toplevel(self.root)

            def quit_received_req():
                display_received_req.withdraw()
                self.root.deiconify()

            display_received_req.protocol("WM_DELETE_WINDOW", quit_received_req)

            received_request = DbmsConnect("priornet")
            received_request.get_data_from_database(f"Select username, user_id from user where user_id in(select fromID"
                                                    f" from request where toID='{self.user_id}')")

            display_friends = tk.Canvas(display_received_req)
            display_friends.pack(side="left", fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(display_received_req, orient="vertical", command=display_friends.yview)
            scrollbar.pack(side="right", fill=tk.Y)

            scrollable_frame = ttk.Frame(display_friends)
            scrollable_frame.bind(
                "<Configure>",
                lambda e: display_friends.configure(
                    scrollregion=display_friends.bbox("all")
                )
            )
            display_friends.create_window((0, 0), window=scrollable_frame, anchor="nw")
            display_friends.configure(yscrollcommand=self.scrollbar.set)

            req_list = received_request.data
            row = 0
            user_count = 0

            def accept(idx):
                name = req_list[idx][0]
                id = req_list[idx][1]
                accept_request = DbmsConnect("priornet")
                try:
                    accept_request.insert_into_database(f"insert into friends values('{user_id}','{id}')")
                except:
                    messagebox.showwarning("Already Friend", f"{name} is already your friend!")
                accept_request.insert_into_database(f"Delete from request where toID ='{user_id}' and fromID='{id}'")
                display_received_req.withdraw()
                received_requests()

            def decline(idx):
                # name = req_list[idx][0]
                id = req_list[idx][1]
                decline_request = DbmsConnect("priornet")
                decline_request.insert_into_database(f"Delete from request where toID ={user_id} and fromID={id}")
                display_received_req.withdraw()
                received_requests()

            for name, id in received_request.data:
                frnd_name = ''.join(name)
                frnd_name_lbl = tk.Label(scrollable_frame, text=frnd_name)
                frnd_name_lbl.grid(row=row, column=0, padx=(10, 100))
                #
                accept_btn = tk.Button(scrollable_frame,text="Accept",
                                       command=functools.partial(accept, idx=user_count))
                accept_btn.grid(row=row, column=1, padx=5)

                decline_btn = tk.Button(scrollable_frame,text="Decline",
                                        command=functools.partial(decline, idx=user_count))
                decline_btn.grid(row=row, column=2, padx=5)

                separator = ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL)
                separator.grid(row=row + 1, column=0, columnspan=4, padx=(5, 0), pady=5, sticky="ew")
                row += 2
                user_count += 1

            display_received_req.mainloop()

        self.requests = tk.Button(self.upper_seg, text="Received requests", command=received_requests)
        self.requests.grid(column=1, row=1, sticky="e", padx=5)

        self.search_entry = tk.Entry(self.upper_seg, font=("Calibri", 12))
        self.search_entry.grid(column=0, row=2, padx=5, pady=5, sticky="ew")

        def search_users():
            name = self.search_entry.get()
            FLAG = True
            if name != "":
                for friend_id, friend_name in self.user_list.items():
                    if name.lower() == friend_name.lower():
                        for widget in self.scrollable_frame.winfo_children():
                            widget.destroy()
                        FLAG = False
                        searched_friend = ((friend_name, friend_id),)
                        print("in")
                        self.display_non_friend_users(searched_friend)

            else:
                messagebox.showwarning("Search", "No username given")
                FLAG = False
            if FLAG:
                messagebox.showwarning("Search", "Friend not found")

        self.search_button = tk.Button(self.upper_seg, text="Search users", command=search_users)
        self.search_button.grid(column=1, row=2, padx=5, pady=5, sticky="w")

        self.separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.separator.pack(fill=tk.X, padx=10)

        self.lower_seg = tk.Frame(self.root)
        self.lower_seg.pack(fill=tk.X)
        tk.Grid.columnconfigure(self.lower_seg, 0, weight=1)
        tk.Grid.columnconfigure(self.lower_seg, 1, weight=1)
        # tk.Grid.columnconfigure(self.lower_seg, 2, weight=1)
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

        self.userdetails = DbmsConnect("priornet")
        self.userdetails.get_data_from_database(f"select username, user_id from user where user_id not in "
                                                f"(select FriendIDs from friends where UID = '{self.user_id}'or "
                                                f"FriendIDs ='{self.user_id}') and user_id not in (select UID from "
                                                f"friends where UID = '{self.user_id}'or FriendIDs='{self.user_id}')")

        self.display_non_friend_users(self.userdetails.data)

    def display_non_friend_users(self, user_list):
        row = 0
        user_count = 0

        def profile(idx):
            UserProfile(user_list[idx][0], user_list[idx][1])

        def send_request(idx):
            friend_name = user_list[idx][0]
            friend_id = user_list[idx][1]
            try:
                sent_request = DbmsConnect("Priornet")
                sent_request.insert_into_database(f"insert into request values('{self.user_id}', '{friend_id}')")
                messagebox.showinfo("Sent!", "Request sent!")
            except mysql.connector.errors.IntegrityError:
                messagebox.showwarning("Request pending!", "Friend request already sent!")
            except mysql.connector.errors.DatabaseError:
                messagebox.showinfo("Request received", "You have received friend request from this user")

        try:
            for name, id in user_list:
                frnd_name = ''.join(name)
                if frnd_name != self.username:
                    self.user_list[''.join(id)] = frnd_name

                    frnd_name_lbl = tk.Label(self.scrollable_frame, text=frnd_name)
                    frnd_name_lbl.grid(row=row, column=0, padx=(10, 100))

                    profile_btn = tk.Button(self.scrollable_frame,
                                            text="See Profile", command=functools.partial(profile, idx=user_count))
                    profile_btn.grid(row=row, column=1, padx=5)

                    add_friend_btn = tk.Button(self.scrollable_frame,
                                               text="Add to Friend",
                                               command=functools.partial(send_request, idx=user_count))
                    add_friend_btn.grid(row=row, column=2, padx=5)

                    separator = ttk.Separator(self.scrollable_frame, orient=tk.HORIZONTAL)
                    separator.grid(row=row + 1, column=0, columnspan=4, padx=(5, 0), pady=5, sticky="ew")
                    row += 2
                user_count += 1
        except Exception as e:
            print(e)
            no_user = tk.Label(self.scrollable_frame, text="No user to show!")
            no_user.grid(row=0, column=0)

        self.root.mainloop()

# root = tk.Tk()
#
# win = tk.Toplevel(root)
#
# AddFriend(root, win, "PN000001", "Roronoa")
#
# root.mainloop()

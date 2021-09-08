import functools
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image
import shutil
import os
import datetime

from Code.DBMS_Connect import DbmsConnect
from Code.userprofile import UserProfile

class NewsFeed:
    IMG_PATH = r"D:\Study material\miniproject\PriorNet\Data\Photos"
    Images = r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images"
    X = datetime.datetime.now()
    TIME_NOW = X.strftime("%Y") + X.strftime("%m") + X.strftime("%d") + X.strftime("%H") + \
               X.strftime("%M") + X.strftime("%S")
    DATE_OF_UPLOAD = X.strftime("%Y-%m-%d")
    image_name = ""
    post_id = ''

    def __init__(self, master, root, user_id, username):
        self.user_id = user_id
        self.username = username
        self.win = root
        self.win.title("PriorNet-Newsfeed")
        self.win.geometry("1000x600+400+200")

        def quit_news_feed():
            self.win.withdraw()
            children_widgets = self.win.winfo_children()
            for child_widget in children_widgets:
                if child_widget.winfo_class() == 'Entry':
                    child_widget.delete(0, tk.END)
            master.deiconify()

        self.win.protocol("WM_DELETE_WINDOW", quit_news_feed)

        tk.Grid.columnconfigure(self.win, 0, weight=1)
        tk.Grid.columnconfigure(self.win, 1, weight=1)

        # Left Frame for profile---------------------------------------------------------------------------
        self.left_frame = tk.Frame(self.win, highlightbackground="Grey", highlightthickness=2)
        self.left_frame.pack(fill=tk.Y, side=tk.LEFT)
        tk.Grid.columnconfigure(self.left_frame, 0, weight=1)

        img_path = DbmsConnect("priornet")
        img_path.get_data_from_database(f"Select photo from profile where user_id='{user_id}'")
        try:
            for img in img_path.data:
                imgg = ''.join(img)
            image = Image.open(os.path.join(self.IMG_PATH, self.username, imgg))
        except Exception as e:
            print(e)
            image = Image.open(os.path.join(self.Images, "profile.jpg"))

        image = image.resize((190, 190))
        image = ImageTk.PhotoImage(image)
        self.image_lbl = tk.Label(self.left_frame, image=image)
        self.image_lbl.grid(column=0, row=0, padx=10, pady=10)

        self.user_label = tk.Label(self.left_frame, text=username)
        self.user_label.grid(column=0, row=1)

        def edit_profile():
            image = filedialog.askopenfilename(title='Select Profile picture')
            if image != "":
                image_name = os.path.basename(image)
                ext = os.path.splitext(image_name)[1]
                exact_path = os.path.join(self.IMG_PATH, self.username)
                shutil.copy(image, exact_path)
                try:
                    os.rename(os.path.join(exact_path, image_name),
                              os.path.join(exact_path, f"Profile_{self.user_id}{ext}"))
                except FileExistsError:
                    os.remove(os.path.join(exact_path, f"Profile_{self.user_id}{ext}"))
                    os.rename(os.path.join(exact_path, image_name),
                              os.path.join(exact_path, f"Profile_{self.user_id}{ext}"))

                image_name = f"Profile_{self.user_id}{ext}"
                update_profile = DbmsConnect("priornet")
                try:
                    update_profile.insert_into_database(f"update profile set photo='{image_name}' where user_id='{self.user_id}'")
                except:
                    messagebox.showerror("Error", "Please,try again later!")
            self.win.withdraw()
            self.win.deiconify()
        self.update_profile_btn = tk.Button(self.left_frame, text="Update profile picture", command=edit_profile)
        self.update_profile_btn.grid(column=0, row=2)

        def back_to_home():
            self.win.withdraw()
            children_widgets = self.win.winfo_children()
            for child_widget in children_widgets:
                if child_widget.winfo_class() == 'Entry':
                    child_widget.delete(0, tk.END)
            master.deiconify()

        self.back_to_home_btn = tk.Button(self.left_frame, text="Back To Home", command=back_to_home)
        self.back_to_home_btn.grid(column=0, row=3)

        # Right frame for newsfeed---------------------------------------------------------------------------
        self.right = tk.Frame(self.win, bg="black")
        tk.Grid.columnconfigure(self.right, 0, weight=1)

        tk.Grid.rowconfigure(self.right, 1, weight=1)
        self.right.pack(fill=tk.BOTH, expand=True)

        # Entry to write status------------------------------------------------------------------------------
        self.right_upper_part = tk.Frame(self.right)
        self.right_upper_part.grid(row=0, column=0, sticky="new")
        tk.Grid.columnconfigure(self.right_upper_part, 0, weight=1)
        tk.Grid.columnconfigure(self.right_upper_part, 1, weight=1)

        self.upload_status = tk.Text(self.right_upper_part, width=50, height=5)
        self.upload_status.grid(column=0, row=0, sticky="WE", padx=10, pady=10)

        self.button_frame = tk.Frame(self.right_upper_part)
        self.button_frame.grid(column=1, row=0, sticky=tk.E)

        def open_img():
            self.FLAG = False
            x = filedialog.askopenfilename(title='open')
            try:
                post_count = DbmsConnect("priornet")
                post_count.get_data_from_database(f"Select post_count from user_count")
                post_count = post_count.data[0][0]
                confirm_text.set("Photo Selected")
                self.image_name = os.path.basename(x)
                print(self.image_name)
                exact_path = os.path.join(self.IMG_PATH, username)
                ext = os.path.splitext(self.image_name)[1]
                if not os.path.exists(exact_path):
                    os.makedirs(exact_path)
                shutil.copy(x, exact_path)
                os.rename(os.path.join(exact_path, self.image_name), os.path.join(exact_path, f"{self.TIME_NOW}_{post_count}{ext}"))
                self.post_id = f"{self.TIME_NOW}_{post_count}"
                self.image_name = f"{self.TIME_NOW}_{post_count}{ext}"
                self.FLAG = True
                self.confirm_label.grid(column=0, row=1)
            except AttributeError:
                messagebox.showwarning("Error", "Some Error occurred")

        self.choose_img_btn = tk.Button(self.button_frame, text="Choose Photo", command=open_img)
        self.choose_img_btn.grid(column=0, row=0, pady=10, padx=5)

        confirm_text = tk.StringVar()
        self.confirm_label = tk.Label(self.right_upper_part, textvariable=confirm_text)

        def upload():
            status = self.upload_status.get("1.0", tk.END)
            self.upload_status.delete("1.0", tk.END)
            if status.strip() != "" or self.image_name.strip() != '':
                try:
                    upload = DbmsConnect("priornet")
                    if status == "":
                        status = "NULL"
                    elif self.image_name == "":
                        self.image_name = "NULL"

                    upload.insert_into_database(f"insert into posts values('{self.post_id}', '{user_id}', '{status}',"
                                                f" '{self.image_name}', '{self.DATE_OF_UPLOAD}')")
                    messagebox.showinfo("Success", "Uploaded successfully")
                    self.confirm_label.grid_remove()
                    self.FLAG = False

                except Exception as e:
                    messagebox.showerror("Failure", "Some error occurred!")
                    print(e)
            else:
                messagebox.showwarning("Empty", "Empty values received")

        self.upload_button = tk.Button(self.button_frame, text="Upload", command=upload)
        self.upload_button.grid(column=0, row=1)

        # for displaying the posts of friends--------------------------------------------------------------------
        self.right_lower_part = tk.Frame(self.right, bg="black")
        self.right_lower_part.grid(row=1, column=0, sticky="nsew")
        try:
            self.friends_details = DbmsConnect('priornet')
            self.friends_details.get_data_from_database(
                f"select U.username, U.user_id, P.Text, P.Image, P.date_of_upload from User U, posts P where P.UID = "
                f"U.user_id and U.user_id in(select user_id from user where user_id in (select FriendIDs from friends "
                f"where UID = '{self.user_id}'or FriendIDs ='{self.user_id}') or user_id in (select UID from friends "
                f"where UID = '{self.user_id}'or FriendIDs='{self.user_id}')) and P.date_of_upload >= "
                f"DATE_SUB(CURDATE(),INTERVAL 7 day) ORDER BY P.PID DESC;")

        except Exception as e:
            print("[Exception in Newsfeed]", e)

        self.display_posts = tk.Canvas(self.right_lower_part, bg="white")
        self.display_posts.pack(side="left", fill=tk.BOTH, expand=True)

        self.display_posts.update()
        screen_width = self.display_posts.winfo_width()

        self.scrollbar = ttk.Scrollbar(self.right_lower_part, orient="vertical", command=self.display_posts.yview)
        self.scrollbar.pack(side="right", fill=tk.Y)

        self.scrollable_frame = ttk.Frame(self.display_posts)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.display_posts.configure(
                scrollregion=self.display_posts.bbox("all")
            )
        )

        self.display_posts.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=screen_width)
        self.display_posts.configure(yscrollcommand=self.scrollbar.set)

        post_count = 0

        def goto_profile(idx):
            friend_name = self.friends_details.data[idx][0]
            friend_id = self.friends_details.data[idx][1]
            self.win.withdraw()

            UserProfile(self.win, friend_name, friend_id)

        for frn_name, frn_id, text, img, date in self.friends_details.data:
            self.frame = tk.Frame(self.scrollable_frame)
            self.frame.pack()

            if frn_name == self.username:
                self.name_button = tk.Button(self.frame, text="You", borderwidth=0, font=(20,),
                                             command=functools.partial(goto_profile, idx=post_count))
                self.name_button.grid(column=0, row=0, sticky='w')
            else:
                self.name_button = tk.Button(self.frame, text=frn_name, borderwidth=0, font=(20,),
                                             command=functools.partial(goto_profile, idx=post_count))
                self.name_button.grid(column=0, row=0, sticky='w')

            self.date_of_upload = tk.Label(self.frame, text=date)
            self.date_of_upload.grid(column=1, row=0, ipady=10)

            if text != "NULL" and text != "\n":
                self.text_lbl = tk.Label(self.scrollable_frame, text=text)
                self.text_lbl.pack()

            if img != "NULL" and img is not None:
                try:
                    photo = Image.open(os.path.join(self.IMG_PATH, frn_name, img))
                    photo = photo.resize((400, 400))
                    photo = ImageTk.PhotoImage(photo)
                    self.image_lbl = tk.Label(self.scrollable_frame, image=photo, width=screen_width)
                    self.image_lbl.photo = photo
                    self.image_lbl.pack(fill=tk.X)
                except Exception as e:
                    print(e)
                    pass

            separator = ttk.Separator(self.scrollable_frame)
            separator.pack(fill=tk.X)

            post_count += post_count

        self.win.mainloop()


# root = tk.Tk()
#
# win = tk.Toplevel(root)
# NewsFeed(root, win, "PN000000", "Rama")
#
# root.mainloop()

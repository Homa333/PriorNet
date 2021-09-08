import tkinter as tk
from tkinter import Toplevel
import os
from PIL import ImageTk, Image

from Code.DBMS_Connect import DbmsConnect


class UserProfile:
    images = r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images"
    IMG_PATH = r"D:\Study material\miniproject\PriorNet\Data\Photos"

    def __init__(self,root, username, usr_id):
        self.username = username
        self.usr_id = usr_id

        self.win = Toplevel(root)
        self.win.geometry("400x500")
        self.win.title("Profile-" + self.username)
        def close():
            self.win.withdraw()
            self.win.master.deiconify()

        self.win.protocol("WM_DELETE_WINDOW", close)

        try:
            get_user_details = DbmsConnect("priornet")
            get_user_details.get_data_from_database(f"Select U.username, U.gender, U.email, P.first_name, P.last_name, "
                                                    f"P.photo  from user U JOIN profile P ON(U.user_id='{self.usr_id}' "
                                                    f"and P.user_id='{self.usr_id}')")

            for name, gender, email, first_name, last_name, photo_path in get_user_details.data:
                self.username = ''.join(name)
                self.gender = ''.join(gender)
                self.email = ''.join(email)
                self.first_name = ''.join(first_name)
                self.last_name = ''.join(last_name)
                if photo_path != "NULL":
                    self.photo_path = ''.join(photo_path)
                    self.photo_path = os.path.join(self.IMG_PATH, self.username, self.photo_path)
                else:
                    self.photo_path = "profile.jpg"
        except Exception as e:
            print("[test1]", e)

        try:
            image = Image.open(os.path.join(self.IMG_PATH, username, self.photo_path))
        except Exception as e:
            print("[test2]",e)
            image = Image.open(os.path.join(self.images, "profile.jpg"))
        image = image.resize((250, 250))
        self.img = ImageTk.PhotoImage(image)
        self.user_profile = tk.Label(self.win, image=self.img)
        self.user_profile.pack(pady=10)

        self.user_name_lbl = tk.Label(self.win, text=f"Username: {self.username}")
        self.user_name_lbl.pack(pady=5)

        self.name_lbl = tk.Label(self.win, text=f"Name: {self.first_name} {self.last_name}")
        self.name_lbl.pack(pady=5)

        self.gender_lbl = tk.Label(self.win, text=f"Gender: {self.gender}")
        self.gender_lbl.pack(pady=5)

        self.email_lbl = tk.Label(self.win, text=f"Email: {self.email}")
        self.email_lbl.pack(pady=5)

        self.win.mainloop()

# UserProfile("Anku", "PN000001")

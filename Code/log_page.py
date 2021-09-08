import os
import re
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector.errors
from PIL import ImageTk, Image

from resources.Encryption_Decryption import encrypt_decrypt
from Code.DBMS_Connect import DbmsConnect
from Code.home_page import HomePage

# Global variable
DEFAULT_PORT = 1231
IMG_PATH = r"D:\Study material\miniproject\PriorNet\Data\Photos"
Images = r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images"
EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")


class LoginPage:
    def __init__(self, root, where):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.x = self.root.master.winfo_x()
        self.y = self.root.master.winfo_y()

        self.gen = tk.StringVar(value="L")

        if where == "in":
            self.login()
        else:
            self.sign_up()
        self.root.mainloop()

    def login(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.geometry("+%d+%d" % (self.x, self.y))
        self.root.geometry("300x230")
        self.root.title("PriorNet-Login")

        back_img = Image.open(os.path.join(Images, "arrow-back-icon.png"))
        back_img = back_img.resize((30, 30))
        back_img = ImageTk.PhotoImage(back_img)
        tk.Grid.columnconfigure(self.root, 1, weight=1)

        back_btn = tk.Button(self.root, image=back_img, borderwidth=0, command=self.go_back)
        back_btn.photo = back_img
        back_btn.grid(column=0, row=0, padx=5, pady=10, sticky="w")

        login_lbl = tk.Label(self.root, text="Login", font=(20,))
        login_lbl.grid(column=1, row=0, pady=10, sticky="w")

        uname_lbl = tk.Label(self.root, text="User Name/ Email: ")
        uname_lbl.grid(column=0, row=1, pady=5, padx=7, sticky="w")

        uname_entry = tk.Entry(self.root)
        uname_entry.grid(column=0, row=2, columnspan=3, pady=5, padx=7, sticky="nsew")

        password_lbl = tk.Label(self.root, text="Password: ")
        password_lbl.grid(column=0, row=3, pady=5, padx=7, sticky="w")

        password_entry = tk.Entry(self.root, show="*")
        password_entry.grid(column=0, row=4, columnspan=3, pady=5, padx=7, sticky="nsew")

        def login():
            uname = uname_entry.get()
            uname = uname.strip()
            pass_log = password_entry.get()
            pass_log = pass_log.strip()
            flag = True
            if uname == "" or pass_log == "":
                messagebox.showwarning("Login", "Please do not leave any required fields blank.")
            else:
                get_data = DbmsConnect("priornet")
                get_data.get_data_from_database("Select user_id, username, email, port_number, password from user")
                for id1, nam, mail, port, pas in get_data.data:
                    user_id = ''.join(id1)
                    name = ''.join(nam)
                    email = ''.join(mail)
                    if uname == name or uname == email:
                        flag = False
                        password_db = ''.join(pas)
                        password_db = encrypt_decrypt.decrypt_message(password_db)
                        if pass_log == password_db:
                            self.root.withdraw()
                            homepage = tk.Toplevel(self.root)
                            HomePage(homepage, user_id, name, port)
                        else:
                            messagebox.showerror("Login", "Wrong username or password!")
                if flag:
                    messagebox.showerror("Login", "Wrong username or password!")

        log_but = tk.Button(self.root, text="Login", command=login)
        log_but.grid(column=2, row=5, pady=5, padx=7)

    def sign_up(self):
        self.root.title("PriorNet-Signup")
        self.root.geometry("+%d+%d" % (self.x-100, self.y-100))
        # self.root.grid_columnconfigure(0, weight=1)

        back_img = Image.open(os.path.join(Images, "arrow-back-icon.png"))
        back_img = back_img.resize((30, 30))
        back_img = ImageTk.PhotoImage(back_img)

        back_btn = tk.Button(self.root, image=back_img, borderwidth=0, command=self.go_back)
        back_btn.photo = back_img
        back_btn.grid(column=0, row=0, padx=5, pady=10, sticky="w")

        sign_up_lbl = tk.Label(self.root, text="Sign Up", font=(20,))
        sign_up_lbl.grid(column=1, row=0, padx=5, pady=10, sticky="w")

        fname_lbl = tk.Label(self.root, text="First Name: ")
        fname_lbl.grid(column=0, row=1, pady=5, padx=7, sticky="nw")

        fname_entry = tk.Entry(self.root)
        fname_entry.grid(column=0, row=2, columnspan=3, pady=5, padx=7, sticky="nsew")

        lname_lbl = tk.Label(self.root, text="Last Name: ")
        lname_lbl.grid(column=0, row=3, pady=5, padx=7, sticky="w")

        lname_entry = tk.Entry(self.root)
        lname_entry.grid(column=0, row=4, columnspan=3, pady=5, padx=7, sticky="nsew")

        uname_lbl = tk.Label(self.root, text="User Name:")
        uname_lbl.grid(column=0, row=5, pady=5, sticky="w")

        uname_entry = tk.Entry(self.root)
        uname_entry.grid(column=0, row=6, columnspan=3, pady=5, padx=7, sticky="nsew")

        gender_frame = tk.Frame(self.root)
        gender_frame.grid(column=0, row=7, pady=5, padx=7, sticky="w")

        gender_lbl = tk.Label(gender_frame, text="Gender: ")
        gender_lbl.pack(side=tk.LEFT)

        genders = [
            ("Male", "M"),
            ("Female", "F"),
            ("Other", "O"),
        ]

        for text, mode in genders:
            gender_option = tk.Radiobutton(gender_frame, text=text,
                                           variable=self.gen, value=mode, tristatevalue=0)
            gender_option.pack(side=tk.LEFT)

        email_lbl = tk.Label(self.root, text="Email: ")
        email_lbl.grid(column=0, row=8, pady=5, padx=7, sticky="w")

        email_entry = tk.Entry(self.root)
        email_entry.grid(column=0, row=9, columnspan=3, pady=5, padx=7, sticky="nsew")

        password_lbl = tk.Label(self.root, text="Password:")
        password_lbl.grid(column=0, row=10, pady=5, padx=7, sticky="w")

        password_entry = tk.Entry(self.root, show="*")
        password_entry.grid(column=0, row=11, columnspan=3, pady=5, padx=7, sticky="nsew")

        def signup():
            get_user_count = DbmsConnect("priornet")
            get_user_count.get_data_from_database("Select count from user_count")
            for i in get_user_count.data:
                user_count = i[0]
            uid = "PN" + str(user_count).zfill(6)
            f_name = fname_entry.get()
            l_name = lname_entry.get()
            uname = uname_entry.get()
            uname.strip()
            gender = str(self.gen.get())
            email = email_entry.get()
            email.strip()
            pass_sign = password_entry.get()
            pass_sign.strip()
            if f_name == "" or l_name == "" or uname == "" or email == "" or pass_sign == "" or gender == "":
                messagebox.showwarning("Signup", "Please do not leave any required fields blank.")
            elif len(uname) <= 3:
                messagebox.showwarning("Warning", "Username too short")
            elif len(uname) > 15:
                messagebox.showwarning("Warning", "Username too long")
            elif len(pass_sign) < 8:
                messagebox.showwarning("Warning", "Password too short")
            elif len(pass_sign) > 20:
                messagebox.showwarning("Warning", "Password too long")
            elif not re.search(r"[0-9]", pass_sign):
                messagebox.showwarning("Warning", "Make sure your password has a number in it")
            elif not re.search(r"[A-Z]", pass_sign):
                messagebox.showwarning("Warning", "Make sure your password has a capital letter in it")
            elif not EMAIL_REGEX.match(email):
                messagebox.showwarning("Warning", "Invalid Email Address")

            else:
                try:
                    signup_data = DbmsConnect("priornet")
                    pass_sign = encrypt_decrypt.encrypt_message(pass_sign)
                    signup_data.insert_into_database(f"insert into user values('{uid}', '{uname}','{gender}'"
                                                     f",'{email}',{DEFAULT_PORT + user_count},'{pass_sign}')")

                    image = filedialog.askopenfilename(title='Select Profile picture')
                    exact_path = os.path.join(IMG_PATH, uname)
                    if not os.path.exists(exact_path):
                        os.makedirs(exact_path)
                    if image != "":
                        image_name = os.path.basename(image)
                        shutil.copy(image, exact_path)
                        ext = os.path.splitext(image_name)[1]
                        os.rename(os.path.join(exact_path, image_name),
                                  os.path.join(exact_path, f"Profile_{uid}{ext}"))
                        image_name = f"Profile_{uid}{ext}"
                    else:
                        image_name = "NULL"

                    signup_data.insert_into_database(f"insert into profile values('{uid}', '{f_name}', '{l_name}', "
                                                     f"'{image_name}')")

                    messagebox.showinfo("Success", "Signup Successful")

                    children_widgets = self.root.winfo_children()
                    for child_widget in children_widgets:
                        if child_widget.winfo_class() == 'Entry':
                            child_widget.delete(0, tk.END)
                    self.gen = tk.StringVar(value="L")
                    self.root.withdraw()
                    self.root.master.deiconify()

                except mysql.connector.IntegrityError:
                    messagebox.showerror("error", "Username/Email already exists")
                except mysql.connector.errors.DataError:
                    messagebox.showerror("error", "Username too long")

        note_lbl = tk.Label(self.root, justify=tk.LEFT, text="Note:\n"
                                                             "1) Username should be at least of 4 characters"
                                                             " and less than\n 15 characters\n"
                                                             "2) Password should be alphanumeric and contain"
                                                             " at least \n  capital letter, 8 characters and"
                                                             " less than 20 characters\n"
                            )
        note_lbl.grid(column=0, row=13, sticky="w", padx=5)

        sign_btn = tk.Button(self.root, text="SignUp", command=signup)
        sign_btn.grid(column=2, row=14, padx=5, pady=7, sticky="e")

    def go_back(self):
        self.gen = tk.StringVar(value="L")
        self.root.withdraw()
        children_widgets = self.root.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                child_widget.delete(0, tk.END)
        self.root.master.deiconify()

    def quit_app(self):
        msg_box = messagebox.askquestion("Exit", "Are you sure you want to exit?", icon='warning')
        if msg_box == "yes":
            self.root.master.master.destroy()

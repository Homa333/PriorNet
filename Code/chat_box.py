import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
import errno
import sys
from threading import Thread
from PIL import Image, ImageTk

HEADER = 10  # buffer for receiving message
IP = "localhost"
PORT = 12345


class ChatBox:
    run = True

    def __init__(self, client, master, win, user):
        self.messages = []
        self.client = client
        self.username = user.encode("utf-8")
        self.username_header = f"{len(self.username):<{HEADER}}".encode("utf-8")
        self.client.send(self.username_header + self.username)

        self.root = win
        self.root.title("Chat")

        def on_closing():
            self.run = False
            self.client.close()
            master.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        def get_back():
            self.run = False
            self.root.withdraw()
            self.client.close()
            master.deiconify()

        img = Image.open(r"D:\Study material\miniproject\PriorNet\PriorNet\resources\Images\arrow-back-icon.png")
        img = img.resize((30, 30))
        img = ImageTk.PhotoImage(img)

        goback_btn = tk.Button(top_frame, image=img, borderwidth=0, command=get_back)
        goback_btn.pack(side=tk.LEFT, padx=10, pady=10)

        top_label = tk.Label(top_frame, text="Priornet-Chatroom", foreground="red", font='sans-serif 18 bold')
        top_label.pack(after=goback_btn, padx=10, pady=10)

        self.user_label = tk.Label(top_frame)
        self.user_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # Frame for chat box
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5)

        self.chat_view = scrolledtext.ScrolledText(chat_frame, wrap="word", padx=5, pady=5)
        self.chat_view.config(state=tk.DISABLED)
        self.chat_view.tag_configure('tag-center', justify='center')
        self.chat_view.tag_configure('tag-right', justify='right', background='#ffffd0', spacing1=5, spacing3=5)
        self.chat_view.tag_configure('tag-left', justify='left', background='#d0ffff', spacing1=5, spacing3=5)
        self.chat_view.pack(fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        tk.Grid.columnconfigure(bottom_frame, 0, weight=1)

        chat_entry = tk.Entry(bottom_frame, font='sans-serif 12 bold', width=50)
        chat_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        def clicker():
            try:
                message = chat_entry.get()
                if message != "":
                    msg = message.encode('utf-8')
                    message_header = f"{len(msg):<{HEADER}}".encode('utf-8')
                    self.client.send(message_header + msg)

                    self.chat_view.configure(state='normal')
                    self.chat_view.insert(tk.END, message + "\n", 'tag-right')
                    chat_entry.delete(0, tk.END)
            except ConnectionResetError:
                try:
                    self.client.connect((IP, PORT))
                except Exception as e:
                    print("bhitra", e)
                    pass
                messagebox.showerror("Connection Error", "Disconnected from server. Try Again!")
            except ConnectionAbortedError:
                try:
                    self.client.connect((IP, PORT))
                except Exception as e:
                    print("bhitra", e)
                    pass
                messagebox.showerror("Connection Error", "Disconnected from server. Try Again!")
            except Exception as e:
                print("naya error", e)

            self.chat_view.configure(state='disabled')

        send_but = tk.Button(bottom_frame, text="Send", font='sans-serif 8 bold', command=clicker)
        send_but.grid(row=0, column=1, padx=5, pady=5)

        try:
            receive_thread = Thread(target=self.receive_message)
            receive_thread.start()

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()

        self.root.mainloop()

    def receive_message(self):
        user_count = self.client.recv(HEADER)
        user_count = int(user_count.decode('utf-8').strip())

        user_count = str(user_count - 1)
        self.user_label['text'] = "User Count: " + user_count
        while self.run:
            try:
                username_header = self.client.recv(HEADER)

                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())

                username = self.client.recv(username_length).decode('utf-8')

                message_header = self.client.recv(HEADER)
                message_length = int(message_header.decode('utf-8').strip())
                message = self.client.recv(message_length).decode('utf-8')

                user_count1 = self.client.recv(HEADER)
                user_count1 = int(user_count1.decode('utf-8').strip())
                user_count1 = str(user_count1 - 1)
                self.user_label['text'] = "User Count: " + user_count1

                self.chat_view.configure(state='normal')
                if message == "{joined}":
                    self.chat_view.insert(tk.END, f'{username} has joined the chatroom\n', 'tag-center')
                elif message == "{left}":
                    self.chat_view.insert(tk.END, f'{username} has left the chatroom\n', 'tag-center')
                else:
                    self.chat_view.insert(tk.END, f'{username}:\n{message}\n', 'tag-left')
                self.chat_view.configure(state='disabled')

            except Exception as e:
                pass

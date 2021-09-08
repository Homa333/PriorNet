import errno
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext, messagebox
import socket
import sys

local_host = "127.0.0.1"
HEADER = 10
BUFSIZ = 1024

class ChatWith:
    run = True

    def __init__(self, name, user_port, to_name, to_port):
        self.name = name
        self.user_port = user_port
        self.to_name = to_name
        self.to_port = to_port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((local_host, int(self.user_port)))
        except:
            pass

        self.root = tk.Tk()
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_pathname(self.root.winfo_id()))
        self.root.geometry("500x500")
        self.root.title("Chat")

        def on_closing():
            chat = self.chat_view.get("1.0", "end-1c")
            with open("file.txt", "w") as file:
                for line in chat:
                    file.write(line)
            self.sock.close()
            self.run = False
            self.root.withdraw()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        frnd_name_Label = tk.Label(top_frame, text=to_name, foreground="red", font='sans-serif 18 bold')
        frnd_name_Label.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame for chat box
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5)

        self.chat_view = scrolledtext.ScrolledText(chat_frame, width=20, wrap=tk.WORD)
        self.chat_view.config(state=tk.DISABLED)
        self.chat_view.pack(fill=tk.BOTH, expand=True)

        self.chat_view.tag_configure('tag-name', justify='right', spacing1=0, spacing3=0)
        self.chat_view.tag_configure('tag-right', justify='right', background='#ffffd0', spacing1=0, spacing3=0)
        self.chat_view.tag_configure('tag-left', justify='left', background='#d0ffff', spacing1=0, spacing3=0)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        tk.Grid.columnconfigure(bottom_frame, 0, weight=1)

        chat_entry = tk.Entry(bottom_frame, font='sans-serif 12 bold', width=50)
        chat_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        def clicker():
            self.chat_view.configure(state='normal')
            message = chat_entry.get()
            message = message.strip()
            if message != "":
                self.chat_view.insert(tk.END, "You:\n", "tag-name")
                self.chat_view.insert(tk.END, message + "\n", 'tag-right')
                self.chat_view.yview(tk.END)
                chat_entry.delete(0, tk.END)
                self.send_message(message)

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
            print("[Exception in receive_thread]",e)
            messagebox.showinfo("Error", "Some error occurred!\n Please try again")

        self.root.mainloop()

    def send_message(self, message):
        username_header = f"{len(self.name):<{HEADER}}".encode("utf-8")
        message = message.encode('utf-8')
        self.sock.sendto(username_header+self.name.encode("utf-8")+message, (local_host, self.to_port))

    def receive_message(self):
        while self.run:
            try:

                message, addr = self.sock.recvfrom(BUFSIZ)
                print(message)
                message = message.decode("utf_8")
                print(message)
                username_header = int(message[:HEADER].strip())
                print(username_header)
                username = message[HEADER:HEADER+username_header]
                print(username)

                data = message[HEADER+username_header:]

                if addr[1] == self.to_port:
                    self.chat_view.configure(state='normal')
                    self.chat_view.insert(tk.END, f'{self.to_name}:\n', 'tag-friend')
                    self.chat_view.insert(tk.END, f'{data}\n', 'tag-left')
                else:
                    messagebox._show(f"{username}", f"{username} says: {data}")

                self.chat_view.configure(state='disabled')
            except ConnectionResetError:
                pass
            except OSError as e:
                print("[Exception in chat_with]", e)
                break
            except Exception as e:
                print("[new Exception in chat_with]", e)

# ChatWith("Radha", 1234, "Rama", 1231)
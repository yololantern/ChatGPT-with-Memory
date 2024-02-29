import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from openai import OpenAI

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.client = self.setup_openai_client()
        self.messages = []

    def setup_ui(self):
        self.root.title("Chat with GPT")
        self.text_area = scrolledtext.ScrolledText(root, state='disabled', height=20, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.entry = tk.Entry(root)
        self.entry.bind("<Return>", self.on_send)
        self.entry.grid(row=1, column=0, sticky="nsew", padx=5)
        
        self.progressbar = ttk.Progressbar(root, mode="indeterminate")
        self.progressbar.grid(row=1, column=1, sticky="ew", padx=5)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

    def setup_openai_client(self):
        try:
            with open('key.txt', 'r') as r:
                key = r.read().rstrip('\n')
            client = OpenAI(api_key=key)
            return client
        except FileNotFoundError:
            print("Error: You need to put your API key in a file named 'key.txt'.")
            return None

    def on_send(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.update_conversation("User: " + user_input)
        self.entry.delete(0, tk.END)
        
        self.messages.append({"role": "user", "content": user_input})
        threading.Thread(target=self.chat_with_gpt).start()

    def chat_with_gpt(self):
        self.update_progressbar(True)
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=self.messages
        )
        resp = response.choices[0].message.content
        self.update_progressbar(False)
        self.update_conversation("AI: " + resp)
        
    def update_conversation(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.yview(tk.END)
        self.text_area.configure(state='disabled')

    def update_progressbar(self, active):
        if active:
            self.progressbar.start(10)
        else:
            self.progressbar.stop()

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
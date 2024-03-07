import tkinter as tk
from tkinter import filedialog

from internal.network import connection
import client

class FileStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distributed File Storage System")

        # Create widgets
        self.label = tk.Label(root, text="Choose a file to upload:")
        self.label.pack()

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.download_button = tk.Button(root, text="Download File", command=self.download_file)
        self.download_button.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            client.upload(file_path)
            tk.messagebox.showinfo("Success", "File uploaded successfully")

    def download_file(self):
        # Placeholder for downloading file
        tk.messagebox.showinfo("Info", "Downloading file functionality not implemented yet")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileStorageApp(root)
    root.mainloop()

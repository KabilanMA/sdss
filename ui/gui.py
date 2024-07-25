import tkinter as tk
from tkinter import filedialog, messagebox

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client import upload, fetch_file_names, download_file
from utils.file import extract_data_type


class FileStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distributed File Storage System")

        # widgets
        self.label = tk.Label(root, text="Choose a file to upload:")
        self.label.pack()

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.download_button = tk.Button(root, text="View Files", command=self.open_download_window)
        self.download_button.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            upload(file_path)
            tk.messagebox.showinfo("Success", "File uploaded successfully")

    def open_download_window(self):
        download_window = tk.Toplevel(self.root)
        download_window.title("Files")

        file_names = fetch_file_names()

        headings = ["File Name", "Size (bytes)", "Type", "Download"]
        for i, heading in enumerate(headings):
            heading_label = tk.Label(download_window, text=heading)
            heading_label.grid(row=0, column=i)
        
        for i, (key, value) in enumerate(file_names.items(), start=1):
            # file name
            file_name_label = tk.Label(download_window, text=value[0])
            file_name_label.grid(row=i, column=0)

            # file size 
            file_size_label = tk.Label(download_window, text=value[1])
            file_size_label.grid(row=i, column=1)

            # file type
            file_date_label = tk.Label(download_window, text=extract_data_type(value[0]))
            file_date_label.grid(row=i, column=2)

            # Download button
            download_button = tk.Button(download_window, text="Download", command=lambda v=value[0]: self._download_file(v))
            download_button.grid(row=i, column=3)

    def _download_file(self, file_name):
        if(download_file(file_name)):
            messagebox.showinfo("Info", "Download Completed")
        else:
            messagebox.showinfo("Info", "One or more of the data chunks failed a consistency check. The data may be corrupt.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileStorageApp(root)
    root.mainloop()

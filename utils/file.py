import os


def extract_file_name(file_path: str):
    a = file_path.split("/")
    file_name = a[-1]
    return file_name

def extract_file_size(file_path: str):
    file_size = os.path.getsize(file_path)
    return file_size

def extract_data_type(file_path: str):
    file_name = extract_file_name(file_path)
    data_type = file_name.split('.')[-1]
    return data_type

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
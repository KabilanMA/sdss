from .merkletree import MerkleTree
from config_info import *
import os

def chunk_file(file_path):
    chunks = []
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            chunks.append(data)
    return chunks

def create_chunk_files(file_path):
    file_name = os.path.basename(file_path)
    
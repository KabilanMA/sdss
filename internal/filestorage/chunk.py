from .merkletree import MerkleTree
from config_info import *
import os

# def chunk_file(file_path):
#     chunks = []
#     with open(file_path, 'rb') as file:
#         while True:
#             data = file.read(chunk_size)
#             if not data:
#                 break
#             chunks.append(data)
#     return chunks

def chunk_file(file_path, chunk_size=chunk_size):
    chunks = []
    with open(file_path, 'rb') as file:
        chunk_number = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

def create_chunk_files(file_path):
    file_name = os.path.basename(file_path)
    
from .merkletree import MerkleTree
from config_info import *
import os

def chunk_file(file_path, chunk_size=chunk_size):
    chunks = []
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            if (len(chunk)<chunk_size):
                padding_size = chunk_size - len(chunk)
                padding = b'\x00' * padding_size
                chunk += padding
            chunks.append(chunk)
    return chunks

def create_file_from_chunks(file_path, chunks):
    with open(file_path, "wb") as output_file:
        for chunk in chunks:
            output_file.write(chunk)

def create_file_from_byte(file_path, output_byte):
    with open(file_path, "wb") as output_file:
        output_file.write(output_byte)

def remove_padding(chunk):
    return chunk.rstrip(b'\x00')

def create_chunk_files(file_path):
    file_name = os.path.basename(file_path)
    
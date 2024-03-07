import socket
import threading

from filestorage import chunk
from filestorage.merkletree import MerkleTree

def store_file(file_path):
    chunks = chunk.chunk_file()
    tree = MerkleTree()

    root_hash = tree.get_root_hash(chunks)

    

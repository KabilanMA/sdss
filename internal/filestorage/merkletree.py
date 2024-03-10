import hashlib

class MerkleTree:
    def __init__(self):
        pass

    def _calculate_hash(self, data):
        return hashlib.sha256(data).hexdigest()

    def _build_tree(self, chunks):
        leaves = [self._calculate_hash(chunk) for chunk in chunks]
        tree = leaves[:]
        while len(tree) > 1:
            if (len(tree) % 2 == 0): #even 
                even = True
            else:
                even = False
            temp_tree = []
            for i in range(0, len(tree), 2):
                if (not even):
                    if i >= len(tree)-1:
                        temp_tree.append(self._calculate_hash(tree[i].encode() + tree[i].encode()))
                else:
                    temp_tree.append(self._calculate_hash(tree[i].encode() + tree[i+1].encode()))

            tree = temp_tree[:]
        root_hash = tree[0]
        del leaves, tree
        if isinstance(root_hash, str):
            return root_hash
        return root_hash.decode()

    # def split_file(self, file_path):
    #     chunks = self._chunk_file(file_path)
    #     root_hash = self._build_tree(chunks)
    #     return root_hash, chunks

    # def reconstruct_file(self, root_hash, chunks, output_file):
    #     reconstructed_chunks = []
    #     reconstructed_chunks.extend(chunks)
    #     leaves = [self._calculate_hash(chunk) for chunk in chunks]
    #     tree = leaves[:]
    #     while len(tree) > 1:
    #         tree = [self._calculate_hash(tree[i].encode()+tree[i+1].encode()) for i in range(0, len(tree), 2)]
    #     current_root_hash = tree[0]

    #     if current_root_hash == root_hash:
    #         with open(output_file, 'wb') as file:
    #             for chunk in chunks:
    #                 file.write(chunk)
    #         print("File successfully reconstructed.")

    #     else:
    #         print("File integrity compromised. Reconstruction failed.")

    def get_root_hash(self, chunks):
        return self._build_tree(chunks)
    
    def validate_chunks(self, chunks, root_hash):
        return self._build_tree(chunks) == root_hash

# # Example usage
# if __name__ == "__main__":
#     file_path = 'example.txt'  # Change to your video file path
#     output_file = 'reconstructed_example.txt'  # Change to desired output file path
#     merkle_tree = MerkleTree()
#     root_hash, chunks = merkle_tree.split_file(file_path)
#     print("Root Hash:", root_hash)
#     print("Number of Chunks:", len(chunks))
#     merkle_tree.reconstruct_file(root_hash, chunks, output_file)

#     # a = b"AS"
#     # b = hashlib.sha256(b"AS").hexdigest()
#     # print(b)

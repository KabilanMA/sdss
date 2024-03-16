import hashlib

class MerkleTree:
    def __init__(self):
        pass

    def _calculate_hash(self, data):
        try:
            output = hashlib.sha256(data).hexdigest()
        except TypeError:
            output = hashlib.sha256(data.encode()).hexdigest()
        return output

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


    def get_root_hash(self, chunks):
        return self._build_tree(chunks)
    
    def validate_chunks(self, chunks, root_hash):
        return self._build_tree(chunks) == root_hash
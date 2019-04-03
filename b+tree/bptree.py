class BPlusTree():
    def __init__(self, branch_factor):
        self.branch_factor = branch_factor
        self.root = None
    
    def search(self, x):
        return self.root.search(x)

    """
    def insert(self, pair):
        if self.root == None:
            self.root = Leaf(self.order)
        self.root.insert(pair)
    """
class Node():
    def __init__(self, branch_factor, is_root=False):
        self.branch_factor = branch_factor
        self.is_root = is_root
        
        self.keys = [None] * (branch_factor - 1)
        self.children = [None] * branch_factor
        self.key_num = 0
        self.children_num = 0

class InternalNode(Node):
    def search(self, x):
        for i, k in enumerate(self.keys):
            if x <= k:
                return self.children[i].search



class LeafNode(Node):
    ...
    """
    def insert(self, pair):
        if not self.bucket:  # Empty Bucket
            self.bucket.append(pair)
        else:
            for i, (key, _) in enumerate(self.bucket):
                if key < pair[0]:
                    self.bucket.insert(i-1, pair)
                    break
    """
class Record():
    def __init__(self, data):
        self.data = data

if __name__ == "__main__":
    t = BPlusTree(4)
    
    seven = InternalNode(4, True)
    seven.key_num = 1
    seven.children_num = 2

    threefive = InternalNode(4)
    threefive.key_num = 2
    threefive.children_num = 3

    nine = InternalNode(4)
    nine.key_num = 1
    nine.children_num = 2

    onetwo = LeafNode(4)
    onetwo.key_num = 2
    onetwo.children_num = 3

    threefour = LeafNode(4)
    threefour.key_num = 2
    threefour.children_num = 3

    fivesix = LeafNode(4)
    fivesix.key_num = 2
    fivesix.children_num = 3

    seveneight = LeafNode(4)
    seveneight.key_num = 2
    seveneight.children_num = 3

    nineten = LeafNode(4)
    nineten.key_num = 2
    nineten.children_num = 3

    t.root = seven

    seven.keys[0] =7
    seven.children[0] = threefive
    seven.children[1] = nine

    threefive.keys[0] = 3
    threefive.keys[1] = 5
    threefive.children[0] = onetwo
    threefive.children[1] = threefour
    threefive.children[2] = fivesix

    nine.keys[0] = seveneight
    nine.keys[1] = nineten
    nine.children[0] = seveneight
    nine.children[1] = nineten

    r1 = Record(1)
    r2 = Record(2)
    r3 = Record(3)
    r4 = Record(4)
    r5 = Record(5)
    r6 = Record(6)
    r7 = Record(7)
    r8 = Record(8)
    r9 = Record(9)
    r10 = Record(1)

    onetwo.children[0] = r1
    onetwo.children[1] = r2
    onetwo.children[2] = threefour

    threefour.children[0] = r3
    threefour.children[1] = r4
    threefour.children[2] = fivesix

    fivesix.children[0] = r5
    fivesix.children[1] = r6
    fivesix.children[2] = seveneight

    seveneight.children[0] = r7
    seveneight.children[1] = r8
    seveneight.children[2] = nineten

    nineten.children[0] = r9
    nineten.children[1] = r10
    nineten.children[2] = Record(None)

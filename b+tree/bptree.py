class BPlusTree():
    def __init__(self, branch_factor):
        self.branch_factor = branch_factor
        self.root = None
    def print(self):
        self.root.print(1)
    def search(self, x):
        return self.root.search(x)

    def ranged_search(self, x, y):
        return self.root.ranged_search(x, y)

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
        
        self.keys = []
        self.children = []

class InternalNode(Node):
    def print(self, depth):
        print(depth, self.keys)
        for c in self.children:
            c.print(depth+1)

    def search(self, x):
        print(self.name)
        for i, k in enumerate(self.keys):
            if x < k:
                return self.children[i].search(x)
        return self.children[-1].search(x)
    
    def ranged_search(self, x, y):
        print(self.name)
        for i, k in enumerate(self.keys):
            if x < k:
                return self.children[i].ranged_search(x, y)
        return self.children[-1].search(x, y)


class LeafNode(Node):
    def print(self, depth):
        print(depth, self.keys)

    def search(self, x):
        print(self.name)
        for i, k in enumerate(self.keys):
            if x == k:
                return self.children[i]
        return None

    def ranged_search(self, x, y):
        result = []

        start_index, end_index = 0, len(self.keys) - 1
        start_found, end_found = False, False
        node = self
        while node != None and not end_found:
            print(node.name)
            for i, k in enumerate(node.keys):
                if start_found:
                    start_index = 0
                elif x <= k:
                    start_found = True
                    start_index = i
                else:
                    pass

                if not end_found and y < k:
                    end_found = True
                    end_index = i-1

            if end_index != -1:
                if node.name == "nineten":
                    print(start_index, end_index)
                result += node.children[start_index: end_index+1]
                node = node.children[-1]


        return result


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

    def __str__(self):
        return "Record: " + str(self.data)

def example1():
    t = BPlusTree(4)

    seven = InternalNode(4, True)
    threefive = InternalNode(4)
    nine = InternalNode(4)

    onetwo = LeafNode(4)
    threefour = LeafNode(4)
    fivesix = LeafNode(4)
    seveneight = LeafNode(4)
    nineten = LeafNode(4)

    r1 = Record(1)
    r2 = Record(2)
    r3 = Record(3)
    r4 = Record(4)
    r5 = Record(5)
    r6 = Record(6)
    r7 = Record(7)
    r8 = Record(8)
    r9 = Record(9)
    r10 = Record(10)

    t.root = seven

    seven.keys.append(7)
    seven.children.append(threefive)
    seven.children.append(nine)

    threefive.keys.append(3)
    threefive.keys.append(5)
    threefive.children.append(onetwo)
    threefive.children.append(threefour)
    threefive.children.append(fivesix)

    nine.keys.append(9)
    nine.children.append(seveneight)
    nine.children.append(nineten)

    onetwo.keys.append(1)
    onetwo.keys.append(2)
    onetwo.children.append(r1)
    onetwo.children.append(r2)
    onetwo.children.append(threefour)

    threefour.keys.append(3)
    threefour.keys.append(4)
    threefour.children.append(r3)
    threefour.children.append(r4)
    threefour.children.append(fivesix)

    fivesix.keys.append(5)
    fivesix.keys.append(6)
    fivesix.children.append(r5)
    fivesix.children.append(r6)
    fivesix.children.append(seveneight)

    seveneight.keys.append(7)
    seveneight.keys.append(8)
    seveneight.children.append(r7)
    seveneight.children.append(r8)
    seveneight.children.append(nineten)

    nineten.keys.append(9)
    nineten.keys.append(10)
    nineten.children.append(r9)
    nineten.children.append(r10)
    nineten.children.append(None)

    seven.name = "Node: seven"
    threefive.name = "Node: threefive"
    nine.name = "Node: nine"
    onetwo.name = "Node: onetwo"
    threefour.name = "Node: threefour"
    fivesix.name = "Node: fivesix"
    seveneight.name = "Node: seveneight"
    nineten.name = "Node: nineten"

    return t

def search_test():
    t = example1()
    for i in range(1, 11):
        print("search: ", i)
        print(t.search(i))
        print()

def ranged_search_test():
    t = example1()
    for i in range(2, 11):
        result = t.ranged_search(1, i)
        for x in result:
            print(x, end=', ')
        print()

if __name__ == "__main__":
    t = example1()
    t.print()

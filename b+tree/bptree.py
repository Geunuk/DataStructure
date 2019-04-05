import math
import random

class BPlusTree():
    def __init__(self, branch_factor):
        self.branch_factor = branch_factor
        self.root = None
    def print(self):
        self.root.print(0)
    def test(self):
        self.root.test()
    def insert(self, x, data):
        print("Insert:", x)
        if self.root == None:
            self.root = LeafNode(self, self.branch_factor)
        
        leaf = self.root.leaf_search(x)
        leaf.insert(x, data)
    
    def search(self, x):
        print("Search: ", X)
        return self.root.search(x)

    def ranged_search(self, x, y):
        return self.root.ranged_search(x, y)

class Node():
    def __init__(self, tree, branch_factor):
        self.tree = tree
        self.branch_factor = branch_factor
        self.parent = None
        
        self.keys = []
        self.children = [None]

class InternalNode(Node):
    def print(self, depth):
        print("Depth:", depth, "Keys:", self.keys)
        for c in self.children:
            c.print(depth+1)
    
    def test(self):
        m = len(self.children)
        assert(len(self.keys) == m-1)
        assert(m <= self.branch_factor)
        if self.parent == None:
            assert(2 <= m)
        else:
            assert(math.ceil(self.branch_factor/2) <= m)

        for k in  self.children[0].keys:
            assert(k < self.keys[0])
       
        for i in range(len(self.keys)-1):
            k1, k2 = self.keys[i], self.keys[i+1]
            for x in self.children[i+1].keys:
                assert(k1 <= x and x < k2)
        
        for k in self.children[-1].keys:
            assert(self.keys[-1] <= k)
       
        for c in self.children:
            c.test()

    def insert(self, x, child):
        for i, k in enumerate(self.keys):
            if x == k:
                print("Error: insert(x) x already exists")
                return
            elif x < k:
                self.keys.insert(i, x)
                if child.keys[0] >= x:
                    self.children.insert(i+1, child)
                else:
                    self.children.insert(i, chlid)
                break
                """
                if i == 0:
                    self.children.insert(1, child)
                else:
                    self.children.insert(i, child)
                break
                """
        else:
            self.keys.append(x)
            self.children.append(child)
        
        # split test
        if len(self.children) > self.branch_factor:
            new_node = InternalNode(self.tree, self.branch_factor)
            new_node.parent = self.parent
            new_node.keys = self.keys[self.branch_factor//2 + 1:]
            del self.keys[self.branch_factor//2 + 1:]
            up_key = self.keys.pop()

            new_node.children = self.children[self.branch_factor//2+1:]
            del self.children[self.branch_factor//2+1:]
            for c in new_node.children:
                c.parent = new_node

            if self.parent == None:
                p = InternalNode(self.tree, self.branch_factor)
                p.keys = [up_key]
                p.children = [self, new_node]

                self.parent = p
                self.tree.root = p
                new_node.parent = p
        
            else:
                self.parent.insert(up_key, new_node)

        
    def leaf_search(self, x):
        for i, k in enumerate(self.keys):
            if x < k:
                result_index = i
                break
        else:
            result_index = -1
        return self.children[result_index].leaf_search(x)
        """
        if isinstance(self.children[0], LeafNode):
            return self.children[result_index]
        else:
            return self.children[result_index].leaf_search(x)
        """
    def search(self, x):
        for i, k in enumerate(self.keys):
            if x < k:
                return self.children[i].search(x)
        return self.children[-1].search(x)
    
    def ranged_search(self, x, y):
        for i, k in enumerate(self.keys):
            if x < k:
                return self.children[i].ranged_search(x, y)
        return self.children[-1].search(x, y)


class LeafNode(Node):
    def print(self, depth):
        print("Depth:", depth, "Keys:", self.keys, "Children:", self.children)

    def test(self):

        m = len(self.children)
        assert(len(self.keys) == m-1)
        assert(m <= self.branch_factor)
        if self.parent == None:
            assert(1 <= m)
        else:
            assert(math.ceil(self.branch_factor/2) <= m)
        
        for i in range(len(self.keys)-1):
            k1, k2 = self.keys[i], self.keys[i+1]
            assert(k1 < k2)
        
    def insert(self, x, data):
        for i, k in enumerate(self.keys):
            if x == k:
                print("Error: insert(x) x already exists")
                return
            elif x < k:
                self.keys.insert(i, x)
                self.children.insert(i, data)
                break
        else:
            self.keys.append(x)
            self.children.insert(-1, data)

        # split test
        if len(self.children) > self.branch_factor:
            new_leaf = LeafNode(self.tree, self.branch_factor)
            new_leaf.parent = self.parent
            new_leaf.keys = self.keys[self.branch_factor//2:]
            del self.keys[self.branch_factor//2:]

            new_leaf.children = self.children[self.branch_factor//2:]
            del self.children[self.branch_factor//2:]
            self.children.append(new_leaf)

            if self.parent == None:
                p = InternalNode(self.tree, self.branch_factor)
                p.keys = [new_leaf.keys[0]]
                p.children = [self, new_leaf]

                self.parent = p
                self.tree.root = p
                new_leaf.parent = p
        
            else:
                self.parent.insert(new_leaf.keys[0], new_leaf)

    def leaf_search(self, x):
        return self

    def search(self, x):
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
                result += node.children[start_index: end_index+1]
                node = node.children[-1]


        return result

class Record():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Record: " + str(self.data)

def example1():
    t = BPlusTree(4)

    seven = InternalNode(4)
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
        print(t.search(i))
        print()

def ranged_search_test():
    t = example1()
    for i in range(2, 11):
        result = t.ranged_search(1, i)
        for x in result:
            print(x, end=', ')
        print()

def insert_test_random(branch_factor, key_num):
    t = BPlusTree(branch_factor)

    key_list = list(range(1, key_num+1))
    random.shuffle(key_list)
    for k in key_list:
        t.insert(k, Record(k))
    t.print()
    t.test()

def insert_test_reverse(branch_factor, key_num):
    t = BPlusTree(branch_factor)
    
    key_list = list(range(1, key_num+1))
    key_list.reverse()

    for k in key_list:
        t.insert(k, Record(k))
        t.print()
        t.test()

def insert_test(branch_factor, key_num):
    t = BPlusTree(branch_factor)

    for k in range(1, key_num+1):
        t.insert(k, Record(k))
        t.print()
        t.test()

if __name__ == "__main__":
    t = BPlusTree(4)
    #insert_test_reverse(4, 4)

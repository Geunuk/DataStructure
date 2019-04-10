import math
import random

class NoKeyExistError(Exception):
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return "{} does not exist".foramt(self.key)

class DuplicateKeyExistError(Exception):
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return "{} already exists".foramt(self.key)

class BPlusTree():
    def __init__(self, branch_factor):
        self.branch_factor = branch_factor
        self.root = LeafNode(self, self.branch_factor)
      
    def print(self):
        self.root.print(0)

    def test(self):
        self.root.test()

    def delete(self, x):
        print("Delete:", x)
        leaf = self.root.leaf_search(x)
        leaf.delete(x)

    def insert(self, x, data):
        print("Insert:", x)
        leaf = self.root.leaf_search(x)
        leaf.insert(x, data)
    
    def search(self, x):
        print("Search:", x)
        leaf = self.root.leaf_search(x)
        return leaf.search(x)

    def ranged_search(self, x, y):
        print("Ranged Search: [{}, {}]".format(x, y))
        leaf = self.root.leaf_search(x)
        return leaf.ranged_search(x, y)

class Node():
    def __init__(self, tree, branch_factor):
        self.tree = tree
        self.branch_factor = branch_factor
        self.parent = None
        
        self.keys = []
        self.children = [None]
    
    def __str__(self):
        return hex(id(self))[-4:]

    def leaf_search(self, x):
        node = self
        while not isinstance(node, LeafNode):
            for i, k in enumerate(node.keys):
                if x < k:
                    node =  node.children[i]
                    break
            else:
                node = node.children[-1]
        return node


class InternalNode(Node):
    def print(self, depth):
        children_ids = [str(c) for c in self.children]
        print("Depth: {} [{}]".format(depth, str(self)), end='\t')
        print("Keys:", self.keys, "Children:", children_ids)

        for c in self.children:
            c.print(depth+1)
    
    def test(self):
        m = len(self.children)

        # Number of keys and children test
        assert(len(self.keys) == m-1)
        assert(m <= self.branch_factor)
        if self.parent == None:
            assert(2 <= m)
        else:
            assert(math.ceil(self.branch_factor/2) <= m)

        # Value of key test
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
    
    def delete(self, deleted_key_idx, deleted_child_idx):
        # If root, 2<= m <= b. If not root, ceil(b/2) <= m <= b
        if self.parent == None:
            is_root = True
            min_children_num = 2
        else:
            is_root = False
            min_children_num = math.ceil(self.branch_factor/2)
        
        if self.parent != None:
            # If its's not root, find index of node at the parent's children list
            for i, k in enumerate(self.parent.keys):
                if self.keys[0] < k:
                    index_at_parent = i
                    break
            else:
                index_at_parent = len(self.parent.children)-1
                
            # Check whether node is located at leftmost or rightmost
            # of parent's children list. And get left and right sibling if exsit
            if index_at_parent == 0:
                is_leftmost = True
            else:
                is_leftmost = False
                left_sibling = self.parent.children[index_at_parent-1]
                left_sibling_num = len(left_sibling.children)
                if left_sibling_num >= min_children_num + 1:
                    is_left_enough = True
                else:
                    is_left_enough = False

            if index_at_parent == len(self.parent.children)-1:
                is_rightmost = True
            else:
                is_rightmost = False
                right_sibling = self.parent.children[index_at_parent+1]
                right_sibling_num = len(right_sibling.children)
                if right_sibling_num >= min_children_num + 1:
                    is_right_enough = True
                else:
                    is_right_enough = False
                
        # Delete key and value at my keys and children list
        deleted_key = self.keys.pop(deleted_key_idx)
        del self.children[deleted_child_idx]


        # if number of children cannot satisfy rule of b+-tree
        # after deletetion, borrow or mergre with left of right
        if is_root and len(self.children) < min_children_num:
            self.children[0].parent = None
            self.tree.root = self.children[0]

        elif not is_root and len(self.children) < min_children_num:
            # Internal node orrow from left
            if not is_leftmost and is_left_enough:
                # Borrow key and child from left sibling
                borrow_key = left_sibling.keys.pop()
                borrow_children = left_sibling.children.pop()

                # Change parent of child
                borrow_children.parent = self

                # Add key and child to my node
                self.keys.insert(0, borrow_key)
                self.children.insert(0, borrow_children)

                # Exchange key value with parent
                my_replace_key = self.keys[0]
                parent_replace_key = self.parent.keys[index_at_parent-1]

                self.keys[0] = parent_replace_key
                self.parent.keys[index_at_parent-1] = my_replace_key
            
            # Internal node borrow from rigt
            elif not is_rightmost and is_right_enough:
                # Borrow key and child from right sibling
                borrow_key = right_sibling.keys.pop(0)
                borrow_children = right_sibling.children.pop(0)

                # Change parent of child
                borrow_children.parent = self

                # Add key and child to my node
                self.keys.append(borrow_key)
                self.children.append(borrow_children)

                # Exchange key value with parent
                my_replace_key = self.keys[-1]
                parent_replace_key = self.parent.keys[index_at_parent]

                self.keys[-1] = parent_replace_key
                self.parent.keys[index_at_parent] = my_replace_key

            # Internal node merge with left
            elif not is_leftmost:
                # Delete key and child at parent node
                deleted_key_idx = index_at_parent - 1
                parent_deleted_key = self.parent.keys[deleted_key_idx]
                self.parent.delete(deleted_key_idx, index_at_parent)
                
                # Change parent of my children to left sibling
                for c in self.children:
                    c.parent = left_sibling
    
                # Merge with left sibling
                left_sibling.keys.append(parent_deleted_key)
                left_sibling.keys.extend(self.keys)
                left_sibling.children.extend(self.children)
            
            # When internal node is leftmost, merger with right
            else:
                # Delete key and child at parent node
                deleted_key_idx = index_at_parent
                parent_deleted_key = self.parent.keys[deleted_key_idx]

                self.parent.delete(deleted_key_idx, 0)
            
                # Change parent of my children to right sibling
                for c in self.children:
                    c.parent = right_sibling

                # Merge with right sibling
                right_sibling.keys.insert(0, parent_deleted_key)
                right_sibling.keys[:0] = self.keys
                right_sibling.children[:0] = self.children[:]
    
    def insert(self, x, child):
        # FInd appropriate index and insert key and data
        for i, k in enumerate(self.keys):
            if x < k:
                self.keys.insert(i, x)
                if child.keys[0] >= x:
                    self.children.insert(i+1, child)
                else:
                    self.children.insert(i, chlid)
                break
        else:
            self.keys.append(x)
            self.children.append(child)
        
        # If number of children is bigger than branch factor, split the node
        if len(self.children) > self.branch_factor:
            # Create new node and insert half of keys and children
            new_sibling = InternalNode(self.tree, self.branch_factor)
            new_sibling.parent = self.parent
            new_sibling.keys = self.keys[self.branch_factor//2+1:]
            new_sibling.children = self.children[self.branch_factor//2+1:]

            # Delete relocated keys and children from node
            # If root does not exist and, middle key may 
            del self.keys[self.branch_factor//2+1:]
            middle_key = self.keys.pop()
            del self.children[self.branch_factor//2+1:]

            # Redesignate parent of new node's children
            for c in new_sibling.children:
                c.parent = new_sibling

            # Insert middle key to the parent
            # If parent does not exist, make internal node
            if self.parent != None:
                self.parent.insert(middle_key, new_sibling)
            else:
                new_parent = InternalNode(self.tree, self.branch_factor)
                new_parent.keys = [middle_key]
                new_parent.children = [self, new_sibling]

                self.parent = new_parent
                new_sibling.parent = new_parent
                self.tree.root = new_parent

class LeafNode(Node):
    def print(self, depth):
        children_ids = [str(c) for c in self.children]
        print("Depth: {} [{}]".format(depth, str(self)), end='\t')
        print("Keys:", self.keys, "Children:", children_ids)

    def test(self):
        m = len(self.children)

        # Number of keys and children test
        assert(len(self.keys) == m-1)
        assert(m <= self.branch_factor)
        if self.parent == None:
            assert(1 <= m)
        else:
            assert(math.ceil(self.branch_factor/2) <= m)
        
        # Value of key test
        for i in range(len(self.keys)-1):
            k1, k2 = self.keys[i], self.keys[i+1]
            assert(k1 < k2)
    
    def delete(self, x):
        for i, k in enumerate(self.keys):
            if x == k:
                deleted_index = i
                break
        else:
            raise NoKeyExistError(x)
    
        # Check whether deleted key is located at first of my key list
        if deleted_index == 0:
            is_first_deleted = True
        else:
            is_first_deleted = False
    
        # If root, 2<= m <= b. If not root, ceil(b/2) <= m <= b
        if self.parent == None:
            is_root = True
            min_children_num = 2
        else:
            is_root = False
            min_children_num = math.ceil(self.branch_factor/2)
    
        # If not root, find index of self at the parent's children list
        if not is_root:
            # If its's not root, find index of node at the parent's children list
            for i, k in enumerate(self.parent.keys):
                if self.keys[0] < k:
                    index_at_parent = i
                    break
            else:
                index_at_parent = len(self.parent.children)-1
            
            # Check whether node is located at leftmost or rightmost
            # of parent's children list. And get left and right sibling if exsit
            if index_at_parent == 0:
                is_leftmost = True
            else:
                is_leftmost = False
                left_sibling = self.parent.children[index_at_parent-1]
                left_sibling_num = len(left_sibling.children)
                if left_sibling_num >= min_children_num + 1:
                    is_left_enough = True
                else:
                    is_left_enough = False
            
            if index_at_parent == len(self.parent.children)-1:
                is_rightmost = True
            else:
                is_rightmost = False
                right_sibling = self.parent.children[index_at_parent+1]
                right_sibling_num = len(right_sibling.children)
                if right_sibling_num >= min_children_num + 1:
                    is_right_enough = True
                else:
                    is_right_enough = False
                
        # Delete key and value at my keys and children list
        deleted_key = self.keys.pop(deleted_index)
        del self.children[deleted_index]

        # If root is leaf, nothing left to do
        if is_root:
            return
    

        # If it's not root and number of children cannot satisfy rule of b+-tree
        # after deletetion, borrow or mergre with left of right
        if len(self.children) < min_children_num:
            # Leaf node borrow from left
            if not is_leftmost and is_left_enough:
                # Borrow key and child from left sibling
                borrow_key = left_sibling.keys.pop()
                borrow_children = left_sibling.children.pop(-2)

                # Add key and child to my node
                self.keys.insert(0, borrow_key)
                self.children.insert(0, borrow_children)
            
                # If first value of key at leaf changed, internal must be changed too 
                self.replace_key(deleted_key, borrow_key)
            
                return

            # Leaf node borrow from right
            elif not is_rightmost and is_right_enough:
                # Borrow key and child from right sibling
                borrow_key = right_sibling.keys.pop(0)
                borrow_children = right_sibling.children.pop(0)

                # Add key and child to my node
                self.keys.append(borrow_key)
                self.children.insert(-1, borrow_children)
        
                # If first value of key at leaf changed, internal must be changed too 
                right_sibling.replace_key(borrow_key, right_sibling.keys[0])
                if borrow_key == self.keys[0]:
                    self.replace_key(deleted_key, borrow_key)
            
                return

            # Leaf node merge with left
            elif not is_leftmost:
                # Merge with left sibling and concatenate between leaves
                left_sibling.keys.extend(self.keys)
                left_sibling.children[-1:] = self.children

                # Delete key and child at parent node
                deleted_key_idx = index_at_parent-1
                self.parent.delete(deleted_key_idx, index_at_parent)
                
                return

            # When internal node is leftmost, merger with right
            else:
                # Merge with right sibling
                right_sibling.keys[:0] = self.keys
                right_sibling.children[:0] = self.children[:-1]
             
                # Concatenate with left cousin
                self.concatenate_left_cousin()
                
                # Delete key and child at parent node
                deleted_key_idx = index_at_parent
                self.parent.delete(deleted_key_idx, 0)
              
                # If first value of key at leaf changed, internal must be changed too 
                if len(self.keys) == 0:
                    right_sibling.replace_key(deleted_key, right_sibling.keys[0])
                
                return

        # If first value of key at leaf changed, internal must be changed too 
        if is_first_deleted:
            new_key = self.keys[deleted_index]
            self.replace_key(deleted_key, new_key)
        
        return

    def concatenate_left_cousin(self):
        grand_parent = self.parent.parent
        if grand_parent != None:
            for k in grand_parent.keys:
                if k == self.parent.keys[0]:
                    index_at_grand_parent = i+1
                    break
            else:
                index_at_grand_parent = 0

            if index_at_grand_parent != 0:
                left_uncle = grand_parent.children[index_at_grand_parent-1]
                left_uncle.children[-1] = self.right_sibling

    def replace_key(self, deleted_key, new_key):
        node = self.parent
        while node != None:
            for i, key in enumerate(node.keys):
                if deleted_key == key:
                    node.keys[i] = new_key
                    return
            else:
                node = node.parent
    
    def insert(self, x, data):
        # FInd appropriate index and insert key and data
        for i, k in enumerate(self.keys):
            if x == k:
                raise DuplicateKeyExistError(x)
            elif x < k:
                self.keys.insert(i, x)
                self.children.insert(i, data)
                break
        else:
            self.keys.append(x)
            self.children.insert(-1, data)

        # If number of children is bigger than branch factor, split the node
        if len(self.children) > self.branch_factor:
            # Create new node and insert half of keys and children
            new_sibling = LeafNode(self.tree, self.branch_factor)
            new_sibling.parent = self.parent
            new_sibling.keys = self.keys[self.branch_factor//2:]
            new_sibling.children = self.children[self.branch_factor//2:]
            
            # Delete relocated keys and children from node
            del self.keys[self.branch_factor//2:]
            del self.children[self.branch_factor//2:]
            self.children.append(new_sibling)

            # Insert first key of new node to the parent
            # If parent does not exist, create internal node
            if self.parent != None:
                self.parent.insert(new_sibling.keys[0], new_sibling)
            else:
                new_parent = InternalNode(self.tree, self.branch_factor)
                new_parent.keys = [new_sibling.keys[0]]
                new_parent.children = [self, new_sibling]

                self.parent = new_parent
                new_sibling.parent = new_parent
                self.tree.root = new_parent
    
    def search(self, x):
        for i, k in enumerate(self.keys):
            if x == k:
                return self.children[i]
        return None
    
    def ranged_search(self, x, y):
        result = []

        start_index, end_index = 0, len(self.keys) - 1
        is_start_found, is_end_found = False, False
        node = self

        # Travrse leaves to find datas meet condition
        while node != None and not is_end_found:
            for i, k in enumerate(node.keys):
                # Find start index to copy
                if is_start_found:
                    start_index = 0
                elif x <= k:
                    is_start_found = True
                    start_index = i

                # Find end index to copy
                if not is_end_found and y < k:
                    is_end_found = True
                    end_index = i-1

            # Copy datas to the result and move to the next node
            if not is_start_found:
                node = node.children[-1]
            elif end_index != -1:
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

def insert_test_right(branch_factor, key_num):
    print("Insert test right: branch_factor {} key_num {}".format(branch_factor, key_num))
    t = BPlusTree(branch_factor)
    for k in range(1, key_num+1):
        t.insert(k, Record(k))
        t.test()

def insert_test_reverse(branch_factor, key_num):
    print("Insert test reverse: branch_factor {} key_num {}".format(branch_factor, key_num))
    t = BPlusTree(branch_factor)
    key_list = list(range(1, key_num+1))
    key_list.reverse()

    for k in key_list:
        t.insert(k, Record(k))
        t.test()

def insert_test_random(branch_factor, key_num):
    print("Insert test random: branch_factor {} key_num {}".format(branch_factor, key_num))
    t = BPlusTree(branch_factor)
    key_list = list(range(1, key_num+1))
    random.shuffle(key_list)

    for k in key_list:
        t.insert(k, Record(k))
        t.test()

def insert_test(branch_factor, key_num):
    insert_test_right(branch_factor, key_num)
    insert_test_reverse(branch_factor, key_num)
    insert_test_random(branch_factor, key_num)

def delete_test_right(branch_factor, key_num):
    print("Delete test right: branch_factor {} key_num {}".format(branch_factor, key_num))
    t = BPlusTree(branch_factor)
    for k in range(1, key_num+1):
        t.insert(k, Record(k))

    for  k in range(1, key_num+1):
        t.delete(k)
        t.test()

def delete_test_reverse(branch_factor, key_num):
    print("Delete test reverse: branch_factor {} key_num {}".format(branch_factor, key_num))
    t = BPlusTree(branch_factor)
    key_list = list(range(1, key_num+1))

    for k in key_list:
        t.insert(k, Record(k))

    key_list.reverse()
    for  k in key_list:
        t.delete(k)
        t.test()

def delete_test_random(branch_factor, key_num):
    print("Delete test random: branch_factor {} key_num {}".format(branch_factor, key_num))
    t = BPlusTree(branch_factor)
    key_list = list(range(1, key_num+1))
    for k in key_list:
        t.insert(k, Record(k))
    

    random.shuffle(key_list)
    #key_list = [3,30,18,28,12,19,6,11,25,17,5,16,13,29,10,15,21,20,26,27]
    for  k in key_list:
        t.delete(k)

        t.test()
    t.print()
def delete_test(branch_factor, key_num):
    delete_test_right(branch_factor, key_num)
    delete_test_reverse(branch_factor, key_num)
    delete_test_random(branch_factor, key_num)

def make_tree(num):
    t = BPlusTree(4)
    for i in range(1, num+1):
        t.insert(i,i); t.print()
    return t

if __name__ == "__main__":
    ...

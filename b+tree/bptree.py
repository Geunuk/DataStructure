import math

from graphviz import *

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
    
    def view(self):
        self.g = Digraph(format='png', name="b+-tree",
                graph_attr={'splines':'false'}, node_attr={'shape':'plaintext'})

        self.subgraph_list = [self.g]
        self.node_index = 0
        self.leaf_index = 0
        self.last_child_index = 0

        self.node_index += 1
        node_name = "node".format(self.node_index)
        self.draw_graph(self.root, None, None, 0)

        for l in self.subgraph_list[1:]:
            self.g.subgraph(l)

        self.g.view()

    def make_label(self, node):
        result_str = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        result_str += "<TR>"

        for i in range(node.branch_factor-1):
            result_str += '<TD ROWSPAN="1" PORT="f{}"></TD> '.format(i)
            if i <= len(node.keys)-1:
                result_str +='<TD>{}</TD>'.format(node.keys[i])
            else:
                result_str += '<TD>  </TD>'

        result_str += '<TD ROWSPAN="1" PORT="f{}"></TD> '.format(node.branch_factor-1)
        result_str += '</TR>'
        result_str += '</TABLE>>'
        return result_str

    def draw_graph(self, n, parent_name, index_at_parent, depth):
        # When max depth updated, create new subgraph
        # If not, find subgraph depending on depth
        max_depth = len(self.subgraph_list) - 1
        if max_depth < depth:
            s = Digraph(graph_attr={'rank':'same'})
            self.subgraph_list.append(s)
        else:
            s = self.subgraph_list[depth]

        # When internal node
        if isinstance(n, InternalNode):    
            # Create node
            self.node_index += 1
            node_name = "node{}".format(self.node_index)
            s.node(node_name, self.make_label(n))

            # When root if not leaf, create edge
            if parent_name != None:
                self.g.edge("{}:f{}".format(parent_name, index_at_parent), node_name)

            for child_index, c in enumerate(n.children):
                self.draw_graph(c, node_name, child_index, depth+1)

        # When leaf node
        else:
            # Creat node
            self.leaf_index += 1
            node_name = 'leaf{}'.format(self.leaf_index)
            s.node(node_name, self.make_label(n))
            
            # When root if not leaf, create edge
            if parent_name != None:
                self.g.edge("{}:f{}".format(parent_name, index_at_parent), node_name)

                # Concatenate leaves
                if self.leaf_index != 1 :
                    prev_leaf = "leaf{}:f{}:s".format(self.leaf_index-1, self.last_child_index)
                    self.subgraph_list[depth].edge(prev_leaf, node_name)

                # Update last index of children list of leaf    
                self.last_child_index = len(n.children) - 1

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
                return (x, self.children[i])
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
                key_result = node.keys[start_index: end_index+1]
                children_result = node.children[start_index: end_index+1]
                result += list(zip(key_result, children_result))
                node = node.children[-1]

        return result

class Record():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Record: " + str(self.data)

if __name__ == "__main__":
    t = BPlusTree(4)
    for i in range(1, 30+1):
        t.insert(i, Record(i))


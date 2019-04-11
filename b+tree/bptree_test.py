import random
import unittest

from bptree import *

class TestBPlusTree(unittest.TestCase):
    def test_tree(self, node):
        if isinstance(node, InternalNode):
            self.test_internal_node(node)
            for c in node.children:
                self.test_tree(c)
        else:
            self.test_leaf_node(node)

    def test_internal_node(self, node):
        self.test_number_of_children(node)
        self.test_key_order(node)
        self.test_children_position(node)

    def test_leaf_node(self, node):
        self.test_number_of_children(node)
        self.test_key_order(node)

    def test_number_of_children(self, node):
        # Number of keys and children test

        m = len(node.children)

        self.assertEqual(len(node.keys), m-1)
        self.assertTrue(m <= node.branch_factor)
        if len(node.keys) == 0:
            self.assertEqual(m,1)
        elif node.parent == None:
            self.assertTrue(2 <= m)
        else:
            self.assertTrue(math.ceil(node.branch_factor/2) <= m)

    def test_key_order(self, node):
        # Order of key test
        for i in range(len(node.keys)-1):
            k1, k2 = node.keys[i], node.keys[i+1]
            self.assertTrue(k1 < k2)

    def test_children_position(self, node):
        # Position of children test
        for k in  node.children[0].keys:
            self.assertTrue(k < node.keys[0])
        for i in range(len(node.keys)-1):
            k1, k2 = node.keys[i], node.keys[i+1]
            for x in node.children[i+1].keys:
                self.assertTrue(k1 <= x and x < k2)
        for k in node.children[-1].keys:
            self.assertTrue(node.keys[-1] <= k)

class TestInsert(TestBPlusTree):
    def __init__(self, *args, **kwargs):
        self.branch_factor = kwargs.pop("branch_factor")
        self.key_count = kwargs.pop("key_count")
        super().__init__(*args, **kwargs)
    
    def setUp(self):
        self.t = BPlusTree(self.branch_factor)
       
    def test_insert_right(self):
        for k in range(1, self.key_count+1):
            self.t.insert(k, Record(k))
            root = self.t.root
            self.test_tree(root)

    def test_insert_reverse(self):
        key_list = list(range(1, self.key_count+1))
        key_list.reverse()

        for k in key_list:
            self.t.insert(k, Record(k))
            root = self.t.root
            self.test_tree(root)

    def test_insert_random(self):
        key_list = list(range(1, self.key_count+1))
        random.shuffle(key_list)

        for k in key_list:
            self.t.insert(k, Record(k))
            root = self.t.root
            self.test_tree(root)

class TestDelete(TestBPlusTree):
    def __init__(self, *args, **kwargs):
        self.branch_factor = kwargs.pop("branch_factor")
        self.key_count = kwargs.pop("key_count")
        super().__init__(*args, **kwargs)
    
    def setUp(self):
        self.t = BPlusTree(self.branch_factor)
        for k in range(1, self.key_count+1):
            self.t.insert(k, Record(k))

    def test_delete_right(self):
        for k in range(1, self.key_count+1):
            self.t.delete(k)
            root = self.t.root
            self.test_tree(root)
        
    def test_delete_reverse(self):
        key_list = list(range(1, self.key_count+1))
        key_list.reverse()
        for k in key_list:
            self.t.delete(k)
            root = self.t.root
            self.test_tree(root)

    def test_delete_random(self):
        key_list = list(range(1, self.key_count+1))
        random.shuffle(key_list)
        for k in key_list:
            self.t.delete(k)
            root = self.t.root
            self.test_tree(root)

class TestSearch(TestBPlusTree):
    def __init__(self, *args, **kwargs):
        self.branch_factor = kwargs.pop("branch_factor")
        self.key_count = kwargs.pop("key_count")
        super().__init__(*args, **kwargs)
        
        self.base_window_size = self.branch_factor + 1

        self.t = BPlusTree(self.branch_factor)
        for k in range(1, self.key_count+1):
            self.t.insert(k, Record(k))

    def test_search_exist(self):
        for k in range(1, self.key_count+1):
            result_key = self.t.search(k)[0]
            self.assertEqual(result_key, k)

    def test_search_not_exist(self):
        not_exist_key = 0
        result = self.t.search(not_exist_key)
        self.assertTrue(result == None)

    def test_ranged_search_increase(self):
        for k in range(1, self.key_count+1):
            answer = tuple(range(1, k+1))
            result = self.t.ranged_search(1,k)
            result_keys = list(zip(*result))[0]
            self.assertEqual(answer, result_keys)

    def test_ranged_search_window(self):
        for i in range(1, self.branch_factor+1):
            window_size = i*self.base_window_size
            for k in range(1, self.key_count+1-window_size):
                answer = tuple(range(k, k+window_size))
                result = self.t.ranged_search(k, k+window_size-1)
                result_keys = list(zip(*result))[0]
                self.assertEqual(answer, result_keys)
    
    def test_ranged_search_random(self):
        for k in range(1, self.key_count//self.branch_factor):
            x = random.randint(1,self.key_count)
            y = random.randint(1,self.key_count)

            answer = tuple(range(x, y+1))
            result = self.t.ranged_search(x, y)
            if len(result) == 0:
                result_keys = ()
            else:
                result_keys = list(zip(*result))[0]

            self.assertEqual(answer, result_keys)

def make_insert_suite(odd_bf, even_bf, key_count):
    suite = unittest.TestSuite()

    suite.addTest(TestInsert("test_insert_right", branch_factor=odd_bf, key_count=key_count))
    suite.addTest(TestInsert("test_insert_reverse", branch_factor=odd_bf, key_count=key_count))
    suite.addTest(TestInsert("test_insert_random", branch_factor=odd_bf, key_count=key_count))
    suite.addTest(TestInsert("test_insert_right", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestInsert("test_insert_reverse", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestInsert("test_insert_random", branch_factor=even_bf, key_count=key_count))
    
    suite.addTest(TestDelete("test_delete_right", branch_factor=odd_bf, key_count=key_count))
    suite.addTest(TestDelete("test_delete_reverse", branch_factor=odd_bf, key_count=key_count))
    suite.addTest(TestDelete("test_delete_random", branch_factor=odd_bf, key_count=key_count))
    suite.addTest(TestDelete("test_delete_right", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestDelete("test_delete_reverse", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestDelete("test_delete_random", branch_factor=even_bf, key_count=key_count))
    
    suite.addTest(TestSearch("test_search_exist", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestSearch("test_search_not_exist", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestSearch("test_ranged_search_increase", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestSearch("test_ranged_search_window", branch_factor=even_bf, key_count=key_count))
    suite.addTest(TestSearch("test_ranged_search_random", branch_factor=even_bf, key_count=key_count))
    
    return suite

if __name__ == '__main__':
    odd_bf = 3
    even_bf = 4
    key_count = 1024

    suite = make_insert_suite(odd_bf, even_bf, key_count)
    unittest.TextTestRunner().run(suite)

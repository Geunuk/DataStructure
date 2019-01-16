import math
import random

_max_level = 0

class Node:
    def __init__(self, value, level):
        self.left = None
        self.right = None
        self.up = None
        self.value = value
        self.level = level

    def print_value(self, mod = 'in'):
        # inorder traversal
        if mod == 'in':
            if self.left:
                self.left.print_value()
            print(self.value, end = ' ')
            if self.right:
                self.right.print_value()

        # preorder traversal
        elif mod == 'pre':
            print(self.value, end = ' ')
            if self.left:
                self.left.print_value()
            if self.right:
                self.right.print_value()
                
        # postorder traversal
        elif mod == 'post':
            if self.left:
                self.left.print_value()
            if self.right:
                self.right.print_value()
            print(self.value, end = ' ')

    def _pretty_print_value(self, pretty):
        def x_appender(level, max_level):
            i = 1
            for j in range(level, max_level):
                for _ in range(i):
                    pretty[j].append('X')
                i *= 2
            
        pretty[self.level-1].append(self.value)

        if self.left:
            self.left._pretty_print_value(pretty)
        else:
            x_appender(self.level, _max_level)

        if self.right:
            self.right._pretty_print_value(pretty)
        else:
            x_appender(self.level, _max_level)
 

class Root(Node):
    def __init__(self, value):
        Node.__init__(self, value, 1)

class Tree:
    numNode = 0

    def __init__(self):
        self.root = None

    def print_tree(self):
        self.root.print_value()

    def pretty_print_tree(self):
        space = int(math.log(self.max(), 10)) + 1

        pretty = [[] for i in range(_max_level)]
        self.root._pretty_print_value(pretty)

        for i in range(_max_level):
            side_string = '-' * sum(2**x for x in range(_max_level - i)) * space
            print(side_string, end='')
            for j in range(2**i):

                print("{0:^{1}}".format(pretty[i][j], space), end='')
                if j == 2**i -1:
                    break
                print(' ' * sum(2**x for x in range(_max_level - i + 1)) * space, end = '')
            print(side_string)

    def insert(self, value):
        global _max_level

        Tree.numNode += 1
        if not self.root:
            self.root = Root(value)
            return


        tmpNode = self.root
        while True:
            if value <= tmpNode.value:
                if not tmpNode.left:
                    tmpNode.left = Node(value, tmpNode.level+1)
                    break
                else:
                    tmpNode = tmpNode.left
            elif value > tmpNode.value:
                if not tmpNode.right:
                    tmpNode.right = Node(value, tmpNode.level+1)
                    break
                else:
                    tmpNode = tmpNode.right
        if _max_level < tmpNode.level+1:
            _max_level = tmpNode.level+1

    def _find(self, value):
        tmpNode = self.root
        while tmpNode:
            if tmpNode.value == value:
                break
            elif tmpNode.value > value:
                tmpNode = tmpNode.left
            else:
                tmpNode = tmpNode.right
        return tmpNode

    def find(self, value):
        result = self._find(value)
        if result:
            print(value, 'exists')
        else:
            print(value, "does not exist")

    def _delete(tmpNode):
        if tmpNode.left == None and tmpNode.right == None:
            return None
        elif tmpNode.left != None and tmpNode.right == None:
            return tmpNode.left
        else:
            return tmpNode.right           
    
    def delete(self, value):
        #tmpNode = self._find(value)
        #if not tmpNode:
        #    print(value, 'does not exist')
        #    return
        
        tmpNode = self.root
        while True:
            print("now", tmpNode.value)
            if value < tmpNode.value:
                if value == tmpNode.left:
                    tmpNode.left = _delete(tmpNode.left)
                    break
                else:
                    tmpNode = tmpNode.left
            elif value > tmpNode.value:
                if value ==  tmpNode.right:
                    tmpNode.right = _delte(tmpNode.right)
                    break
                else:
                    tmpNode = tmpNode.right
            else:
                break

    def min(self):
        tmpNode = self.root
        while tmpNode.left:
            tmpNode = tmpNode.left
        return tmpNode.value

    def max(self):
        tmpNode = self.root
        while tmpNode.right:
            tmpNode = tmpNode.right
        return tmpNode.value


def test(t):
    m = int(input("Max number : "))
    for x in random.sample(range(0, m), m):
        t.insert(x)
    t.pretty_print_tree()
    
if __name__ == '__main__':
    t = Tree()
    test(t)

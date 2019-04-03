class B_Plus_Tree():
    def __init__(self, order):
        self.order = order
        self.root = None

    def insert(self, pair):
        if self.root == None:
            self.root = Leaf(self.order)
        self.root.insert(pair)
class In
class Internal():
    def __init__(self, order):
        self.order = order
        self.bucket = []

class Leaf():
    def __init__(self, order):
        self.order = order
        self.bucket = []

    def insert(self, pair):
        if not self.bucket:  # Empty Bucket
            self.bucket.append(pair)
        else:
            for i, (key, _) in enumerate(self.bucket):
                if key < pair[0]:
                    self.bucket.insert(i-1, pair)
                    break

            
if __name__ == "__main__":
    t = B_Plus_Tree(order=3)
    t.insert((1,1))
    print(t.root.bucket)
    t.insert((2,2))
    print(t.root.bucket)


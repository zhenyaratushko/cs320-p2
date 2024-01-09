class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
        
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left.values)
        if self.right != None:
            size += len(self.right.values)
        return size
    
    def lookup(self, key):
        if key == self.key:
            return self.values
        elif key < self.key and self.left != None:
            return self.left.lookup(key)
        elif key > self.key and self.right != None:
            return self.right.lookup(key)
        else:
            return []
        
    def height(self):
        if self.left == None:
            l = 0
        else:
            l = self.left.height()
            
        if self.right == None:
            r = 0
        else:
            r = self.right.height()
            
        return max(l, r)+1
    
    def total(self):
        if self.left == None and self.right == None:
            return 1
        
        l = 0
        r = 0
        
        if self.left != None:
            l = self.left.total()
            
        if self.right != None:
            r = self.right.total()
 
        return l + r
    
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
        
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.right)            
        print(node.key, ":", node.values)  
        self.__dump(node.left)             

    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, index):
        return self.root.lookup(index)

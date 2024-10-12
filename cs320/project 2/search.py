class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
    
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left) 
        if self.right != None:
            size += len(self.right)
        return size
    
    def lookup(self, key):
        
        if self.key == key:
            return self.values
        
        elif self.key > key and self.left != None:
            return self.left.lookup(key)
        
        elif self.key < key and self.right != None:
            return self.right.lookup(key)
        
        else:
            return []
        
    def __getitem__(self, key):
        return self.lookup.key()
    
    def get_height(self):
        if self.left == None:
            l = 0
        
        else:
            l = self.left.get_height() 
            
        if self.right == None:
            r = 0
        
        else:
            r = self.right.get_height() 
        
        return max(l, r) + 1
    
    def num_nonleaf_nodes(self):
        total = 0
        if self.right == None and self.left == None:
            total +=1
            
        if self.right != None:
            total += self.right.num_nonleaf_nodes()
            
        if self.left != None:
            total += self.left.num_nonleaf_nodes()
        
        return total
    
    def return_top_n_rates(self, n):
        rates_list = []
        rates_list.append(self.key)
        
        if self.right != None:
            rates_list.extend(self.right.return_top_n_rates(n))
        
        if self.left != None:
            rates_list.extend(self.left.return_top_n_rates(n))
        if rates_list == None:
            return []
        
        rates_list.sort(reverse = True)                             
        return rates_list[:n]


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
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)            # 1
        
        self.__dump(node.left)             # 3

    def dump(self):
        self.__dump(self.root)
    
    def __getitem__(self, key):
        return self.root.lookup(key)
    
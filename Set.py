#an ordered set implementation in AVL tree

class Set(object):
    class Node:
        def __init__(self, key):
            self.height = 1
            self.left = None
            self.right = None
            self.key = key

    def __init__(self, root=None):
        self.root = root
        self.size = 0
        
    def _h(self, d):
        return 0 if d is None else d.height
    
    def __len__(self):
        return self.size
    
    def _rightRotate(self, d):
        if d is None or d.left is None:
            return d
        r2 = d; r1 = r2.left
        t1 = r1.left; t2 = r1.right; t3 = r2.right
        r2.left, r2.right = t2, t3
        r1.left, r1.right = t1, r2
        r2.height = max(self._h(t2), self._h(t3)) + 1
        r1.height = max(self._h(t1), self._h(r2)) + 1
        return r1
        
    def _leftRotate(self, d):
        if d is None or d.right is None:
            return d
        r1 = d; r2 = d.right
        t1 = r1.left; t2 = r2.left; t3 = r2.right
        r1.left, r1.right = t1, t2
        r2.left, r2.right = r1, t3
        r1.height = max(self._h(t1), self._h(t2)) + 1
        r2.height = max(self._h(r1), self._h(t3)) + 1
        return r2
        
    def _insert(self, n, key):
        if n is None:
            self.size += 1
            return self.Node(key)
        if n.key == key:
            return n
        if key < n.key:
            n.left = self._insert(n.left, key)
        else:
            n.right = self._insert(n.right, key)
        n.height = max(self._h(n.left), self._h(n.right)) + 1
        if self._h(n.left) - self._h(n.right) > 1:
            if key < n.left.key: #left left case
                return self._rightRotate(n)
            else: #left right case
                n.left = self._leftRotate(n.left)
                return self._rightRotate(n)
        if self._h(n.left) - self._h(n.right) < -1:
            if key > n.right.key: #right right case
                return self._leftRotate(n)
            else: #right left case
                n.right = self._rightRotate(n.right)
                return self._leftRotate(n)
        return n
                
    def _remove(self, n, key):
        if n is None:
            return None
        if key < n.key:
            n.left = self._remove(n.left, key)
        elif key > n.key:
            n.right = self._remove(n.right, key)
        else:
            self.size -= 1
            if n.left is None or n.right is None:
                temp = n.left if n.left is not None else n.right
                n = temp
            else:
                cur = n.right
                while cur.left is not None:
                    cur = cur.left
                n.key = cur.key
                n.right = self._remove(cur.key)
        if n is None:
            return n
        n.height = max(self._h(n.left), self._h(n.right)) + 1
        if self._h(n.left) - self._h(n.right) > 1:
            if self._h(n.left.left) > self._h(n.left.right): #left left case
                return self._rightRotate(n)
            else: #left right case
                n.left = self._leftRotate(n.left)
                return self._rightRotate(n)
        if self._h(n.left) - self._h(n.right) < -1:
            if self._h(n.right.left) < self._h(n.right.right): #right right case
                return self._leftRotate(n)
            else: #right left case
                n.right = self._rightRotate(n.right)
                return self._leftRotate(n)
        return n
                
    def find(self, key):
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return True
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return False
        
    def insert(self, key):
        self.root = self._insert(self.root, key)
     
    def remove(self, key):
        self.root = self._remove(self.root, key)
                
    def clear(self):
        self.root = None
        self.size = 0
     
    def max(self):
        cur = self.root
        while cur is not None and cur.right is not None:
            cur = cur.right
        return cur
                
    def min(self):
        cur = self.root
        while cur is not None and cur.left is not None:
            cur = cur.left
        return cur           



class TreeTest(Set):
    def __init__(self, tree=None):
        super(TreeTest, self).__init__()
        self.tree = tree
    
    def from_serial(self, treelist):
        if len(treelist) == 0:
            return None
        treelist.reverse()
        root = Set.Node(treelist.pop())
        cur = [root]
        while len(cur) > 0:
            next = []
            for n in cur:
                if len(treelist)==0: break
                n.left = None if treelist[-1]=="#" else Set.Node(treelist[-1])
                treelist.pop()
                next.append(n.left)
                if len(treelist)==0: break
                n.right = None if treelist[-1]=="#" else Set.Node(treelist[-1])
                treelist.pop()
                next.append(n.right)
            cur = next
        self.tree = Set()
        self.tree.root = root

    def to_serial(self, print_height=False):
        retVal = []
        cur = [self.tree.root]
        while len(cur) > 0:
            next = []
            for n in cur:
                if print_height:
                    retVal.append("#" if n is None else (str(n.key), n.height))
                else:
                    retVal.append("#" if n is None else str(n.key))
                if n is None:
                    continue
                next.append(n.left); next.append(n.right)
            cur = next
        while len(retVal)>0 and retVal[-1]=='#':
            retVal.pop()
        return retVal


if __name__ == "__main__":
    print "hello"
    
    tree = Set()
    for i in range(28, 0, -2):
        tree.insert(i)
    
    tt = TreeTest(tree=tree)
    print tt.to_serial()
    tt.from_serial(tt.to_serial())
    print tt.to_serial()







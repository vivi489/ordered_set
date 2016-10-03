#an ordered set implementation in AVL tree

from Set import Set

class TreeTest(object):
    def __init__(self, tree=None):
        super(TreeTest, self).__init__()
        self.tree = tree
    
    def get_height(self, root):
        if root is None: return 0
        return max(self.get_height(root.left), self.get_height(root.right)) + 1
    
    def _bst_validate(self, root, lower, upper):
        if root is None: return True
        if not self._bst_validate(root.left, lower, root.key):
            return False
        if (lower is not None and root.key<=lower) or\
            (upper is not None and root.key>=upper):\
            return False
        if not self._bst_validate(root.right, root.key, upper):
            return False
        return True

    def bst_validate(self):
        return self._bst_validate(self.tree.root, None, None)

    def _balance_validate(self, root):
        if root is None: return 0
        left = self._balance_validate(root.left)
        if left == -1: return -1
        right = self._balance_validate(root.right)
        if right == -1: return -1
        if abs(left-right) > 1:
            return -1
        else:
            return max(left, right) + 1

    def balance_validate(self):
        return not self._balance_validate(self.tree.root) == -1

    def height_validate(self):
        if self.tree.root is None: return True
        cur_h = self.get_height(self.tree.root)
        cur = [self.tree.root]
        while len(cur) > 0:
            next = []
            for n in cur:
                if not n.height == cur_h:
                    return False
                if n.left is not None: next.append(n.left)
                if n.right is not None: next.append(n.right)
            cur = next
            cur_h -= 1
        return True

    def from_serial(self, treelist):
        if len(treelist) == 0:
            return None
        treelist.reverse()
        root = Set.Node(treelist.pop())
        tree_size = 1
        cur = [root]
        while len(cur) > 0:
            next = []
            for n in cur:
                if len(treelist)==0: break
                n.left = None if treelist[-1]=="#" else Set.Node(treelist[-1])
                if n.left is not None: tree_size += 1
                treelist.pop()
                next.append(n.left)
                if len(treelist)==0: break
                n.right = None if treelist[-1]=="#" else Set.Node(treelist[-1])
                if n.right is not None: tree_size += 1
                treelist.pop()
                next.append(n.right)
            cur = next
        self.tree = Set()
        self.tree.root = root
        self.tree.size = tree_size
        
        cur = [self.tree.root]
        cur_h = self.get_height(self.tree.root)
        while len(cur) > 0:
            next = []
            for n in cur:
                n.height = cur_h
                if n.left is not None: next.append(n.left)
                if n.right is not None: next.append(n.right)
            cur = next
            cur_h -= 1

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

    def get_size(self):
        return len(self.tree)


if __name__ == "__main__":
    #TODO: test cases
    print \
    """
    1. Tree property tests (bst, height, size, balance)
    2. Functional tests (find, max, min, upper_bound, lower_bound)
    3. random r/w performance test
    """
    
    tree = Set()
    for i in range(28, 0, -2):
        tree.insert(i)
    
    tt = TreeTest(tree=tree)
    print tt.to_serial(print_height=True)
    #tt.from_serial(tt.to_serial())
    #print tt.to_serial()
    print tt.get_size()
    print tt.bst_validate()
    print tt.balance_validate()
    print tt.height_validate()



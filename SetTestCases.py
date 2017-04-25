#an ordered set implementation in AVL tree
from __future__ import print_function
from Set import Set
import numpy as np
from sys import stdout
import time


class TreeTestHelper(object):
    def __init__(self, tree=None):
        super(TreeTestHelper, self).__init__()
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
        cur_h = 0
        cur = [self.tree.root]
        while len(cur) > 0:
            next = []
            cur_h += 1
            for n in cur:
                if n.left is not None: next.append(n.left)
                if n.right is not None: next.append(n.right)
            cur = next
        return cur_h == self.get_height(self.tree.root)

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

    def traverse(self):
        if self.tree.root is None:
            return []
        retVal = []
        cur = self.tree.root
        st = []
        while cur.left is not None:
            st.append(cur)
            cur = cur.left
        while cur is not None:
            retVal.append(cur.key)
            if cur.right is not None:
                cur = cur.right
                while cur.left is not None:
                    st.append(cur)
                    cur = cur.left
            else:
                if len(st) == 0: cur = None
                else: cur = st.pop()
        return retVal


def propertyTest(epochs):
    np.random.seed(long(time.time()))
    print("starting property tests")
    for e in range(epochs):
        print("\rgenerate random tree #%d"%e, end="")
        stdout.flush()
        keys = (np.random.rand(20*epochs - 20*(e+1))*20000).astype(np.int32)
        keys = list(set(keys))
        tree = Set()
        tree.update(keys)
        tree.clear()
        tree.update(keys)
        keys.sort()
        test = TreeTestHelper(tree=tree)
        assert test.get_size()==len(keys), "Property Test Failure: size not matched"
        assert test.bst_validate(), "Property Test Failure: BST is not valid"
        assert test.balance_validate(), "Property Test Failure: unbalanced tree"
        assert test.height_validate(), "Property Test Failure: incorrect tree height"
        assert test.traverse()==keys, "Property Test Failure: incorrect inorder traversal output"
    print("\nproperty tests ended")

def functionalTest(epochs):
    np.random.seed(long(time.time()))
    print("starting functional tests")
    for e in range(epochs):
        print("\rgenerate random tree #%d"%e, end="")
        stdout.flush()
        keys = (np.random.rand(20*epochs - 20*(e+1))*20000).astype(np.int32)
        keys = np.array(list(set(keys)))
        tree = Set()
        tree.update(keys)
        tree.clear()
        tree.update(keys)
        keys.sort()
        rand_queries = set((np.random.rand(20*epochs - 20*(e+1))*20000).astype(np.int32))
        for q in rand_queries:
            if q in keys: assert tree.find(q), "Functional Test Failure: key not found"
            else: assert not tree.find(q), "Functional Test Failure: non-existing key found"
        if len(keys)==0:
            assert len(tree)==0, "Functional Test Failure: tree is not empty given no key"
            continue
        key_max, key_min = keys.max(), keys.min()
        assert tree.max()==key_max, "Functional Test Failure: incorrect max key"
        assert tree.min()==key_min, "Functional Test Failure: incorrect min key"
    print("\nfunctional tests ended")


if __name__ == "__main__":
    #TODO: test cases
    print(
    """
    1. Tree property tests (bst, height, size, balance)
    2. Functional tests (find, max, min, upper_bound, lower_bound)
    3. random r/w performance test
    """
    )
    propertyTest(200)
    functionalTest(200)



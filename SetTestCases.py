#an ordered set implementation in AVL tree

from Set import Set

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
    print "TODO: test cases"
    
    tree = Set()
    for i in range(28, 0, -2):
        tree.insert(i)
    
    tt = TreeTest(tree=tree)
    print tt.to_serial()
    tt.from_serial(tt.to_serial())
    print tt.to_serial()







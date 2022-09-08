import collections
import networkx as nx
import matplotlib.pyplot as plt
 
 
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
 
 
class Tree:
    def __init__(self, root_val):
        root_node = Node(root_val)
        self.root = root_node
     
    def add(self, val, parent_val, position):
        parent = self.find(parent_val)   # find the parent node. We assume that there is no duplicate nodes.
        node = Node(val)
        if position == 0:
            parent.left = node
        if position == 1:
            parent.right = node
 
    def find(self, value):
        que = collections.deque([self.root])
        while que:
            node = que.popleft()
            if node.val == value:
                return node
            if node.left:
                que.append(node.left)
            if node.right:
                que.append(node.right)
        raise KeyError('value not found')
 
 
    # draw the tree. https://zhuanlan.zhihu.com/p/35574577
    def draw(self):
        graph = nx.DiGraph()
        graph, pos = self.create_graph(graph, self.root)
        fig, ax = plt.subplots(figsize=(8, 10))  # 比例可以根据树的深度适当调节
        nx.draw_networkx(graph, pos, ax=ax, node_size=300)
        plt.show()
 
    def create_graph(self, G, node, pos={}, x=0, y=0, layer=1):
        pos[node.val] = (x, y)
        if node.left:
            G.add_edge(node.val, node.left.val)
            l_x, l_y = x - 1 / 2 ** layer, y - 1
            l_layer = layer + 1
            self.create_graph(G, node.left, x=l_x, y=l_y, pos=pos, layer=l_layer)
        if node.right:
            G.add_edge(node.val, node.right.val)
            r_x, r_y = x + 1 / 2 ** layer, y - 1
            r_layer = layer + 1
            self.create_graph(G, node.right, x=r_x, y=r_y, pos=pos, layer=r_layer)
        return (G, pos)
 
 
# 示例：
tree = Tree(6)
tree.add(val=2, parent_val=6, position=0)  # position: 0 means 'left', 1 means 'right'
tree.add(3, 6, 1)
tree.add(13, 2, 0)
tree.add(4, 2, 1)
tree.add(12, 4, 0)
tree.add(0, 4, 1)
tree.add(24, 3, 0)
tree.add(17, 3, 1)
 
tree.draw()
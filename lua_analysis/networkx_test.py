import networkx as nx
import matplotlib.pyplot as plt
#更新全局参数，设置图形大小
plt.rcParams.update({
    'figure.figsize':(8,6)
})

def main():
    # 创建空的无向图
    # G = nx.DiGraph() 
    # G.add_edge("a", "b")
    # G.add_edge("c", "b")
    # nx.draw_networkx(G)
    # plt.show()

    # 拓扑排序
    # G = nx.DiGraph()
    # G.add_edge('x','a', weight=3)
    # G.add_edge('a','c', weight=3)
    # G.add_edge('b','c', weight=5)
    # G.add_edge('b','d', weight=4)
    # G.add_edge('d','e', weight=2)
    # G.add_edge('c','y', weight=2)
    # G.add_edge('e','y', weight=3)
    # print(list(nx.topological_sort(G)))
    # nx.draw_networkx(G)
    # plt.show()
    WS = nx.random_graphs.watts_strogatz_graph(200, 40, 0.3)
    pos = nx.circular_layout(WS)
    nx.draw(WS, pos, with_labels=False, node_size=30, edge_color='b', alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
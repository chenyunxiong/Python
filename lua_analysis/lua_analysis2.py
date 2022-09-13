import json
import glob
import re
import sys
from typing import Dict
import networkx as nx
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QTextBrowser, QTreeView, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QJsonArray, QJsonDocument, QJsonParseError, QJsonValue


# path = "E:\Projects\Python\lua_analysis\\"
path = 'C:\Project\gof\gof_client\Assets\Lua\\'
show_view = 'showView'
show_item = 'showItem'
show_data = 'showData'
show_ctrl = 'showCtrl'
show_mgr = 'showMgr'
show_base = 'showBase'
show_module = 'showModule'
show_other = 'showOther'
show_graph = 'showGraph'

colorList = ['red', 'gold', 'violet', 'pink', 'limegreen', 'darkorange', 'gold', 'violet']

class NodeData():
    name = ''
    parentName = ''

    def __init__(self, name, parentName) -> None:
        self.name = name
        self.parentName = parentName
        pass

class Node():
    name = ''
    children = {}

    def __init__(self, name):
        self.name = name
        self.children = {}
        
    def add_child(self, node):
        if self.name == node.name:
            print("can't add to self")
            return
        if not self.children.__contains__(node.name):
            self.children[node.name] = node
    
    def contain_child(self, nodeName):
        if self.children.__contains__(nodeName):
            return True
        return False

    def get_node(self, nodeName):
        if len(self.children) <= 0:
            if self.name == nodeName:
                return self
            else:
                return None
        else:
            for n in self.children.values():
                return n.get_node(nodeName)
    
    def get_name(self):
        return self.name

    def tostring(self, isRoot):
        dict = None
        if len(self.children) > 0:
            if isRoot:
                dict = {}
                dict[self.name] = {}
                for n in self.children.values():
                    dict[self.name][n.name] = n.tostring(False)
            else:
                dict = {}
                for n in self.children.values():
                    dict[n.name] = n.tostring(False)
        # else:
        #     dict = self.name
        return dict

    def export_as_xml(self):
        pass

class Main():
    name_dict = {}
    mark_dict = {}
    root_node = None
    parse_item = {}
    root_name_list = []

    def check_show_item(self, subName, parentName = None):
        if subName.endswith("Base"):
            return self.parse_item.__contains__(show_base) and self.parse_item[show_base]
        if subName.endswith("Module"):
            return self.parse_item.__contains__(show_module) and self.parse_item[show_module]
        if (subName.endswith("View") or subName.endswith("Panel")):
            return self.parse_item.__contains__(show_view) and self.parse_item[show_view]
        if subName.endswith("Item"):
            return self.parse_item.__contains__(show_item) and self.parse_item[show_item]
        if subName.endswith("Ctrl"):
            return self.parse_item.__contains__(show_ctrl) and self.parse_item[show_ctrl]
        if subName.endswith("Data"):
            return self.parse_item.__contains__(show_data) and self.parse_item[show_data]
        if subName.endswith("Mgr"):
            return self.parse_item.__contains__(show_mgr) and self.parse_item[show_mgr]
        return self.parse_item.__contains__(show_other) and self.parse_item[show_other]
    
    def read_file(self, parse_item):
        self.parse_item = parse_item
        list = glob.glob(path+'**/*.lua', recursive=True)
        for l in list:
            with open(l, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    str = line
                    r_base_class = re.search(r'class\(\"(.*)\"\)', str)
                    r_base2 = re.search(r'class\(\"(.*)\", me.(.*)\)', str)
                    r_base3 = re.search(r'class\(\"(.*)\", GUIBase.(.*)\)', str)
                    if r_base_class:
                        parentName = r_base_class.group(1)
                        if parentName not in self.name_dict.keys():
                            if self.check_show_item(parentName):
                                self.name_dict[parentName] = NodeData(parentName, 'class')

                    if r_base2 != None:
                        parentName = r_base2.group(2)
                        subName = r_base2.group(1)
                        if self.check_show_item(subName):
                            if subName not in self.name_dict.keys():
                                self.name_dict[subName] = NodeData(subName, parentName)
                        else:
                            pass

                    if r_base3 != None:
                        parentName = r_base3.group(2)
                        subName = r_base3.group(1)
                        if self.check_show_item(subName):
                            if subName not in self.name_dict.keys():
                                self.name_dict[subName] = NodeData(subName, parentName)
                        else:
                            pass
    
    def parse_node(self):
        self.root_node = Node('class')
        nodeList = []
        nodeList.append(self.root_node)
        while len(nodeList) > 0:
            tmpKeys = []
            targetNode = nodeList.pop()
            for n in self.name_dict.values():
                if n.parentName == targetNode.name:
                    tmpKeys.append(n.name)
            if len(tmpKeys) <= 0:
                continue
            for key in tmpKeys:
                del self.name_dict[key]
                child_node = Node(key)
                nodeList.append(child_node)
                targetNode.add_child(child_node)

    def draw(self, g, node, node_size):
        if node == None or len(node.children) <= 0:
            return
        node_size -= 2
        for n in node.children.values():
            if n != None:
                g.add_node(n.name, size = node_size, font_size = node_size, node_color = colorList)
                g.add_edge(n.name, node.name)
                self.draw(g, n, node_size)

    def draw_tree(self, node, tree_node):
        if node == None or len(node.children) <= 0:
            return 
        for n in node.children.values():
            if n != None:
                item = QTreeWidgetItem(tree_node)
                item.setText(0, n.name)
                self.draw_tree(n, item)

    def drow_map(self, g, tree_root):
        node_size = 10
        self.draw(g, self.root_node, node_size)
        tmpDict = self.root_node.tostring(True)
        txt = json.dumps(tmpDict)
        self.draw_tree(self.root_node, tree_root)
            
        # self.tree = QTreeWidget()
        # self.root_widget = QTreeWidgetItem(self.tree)
        # self.tree.show()

        
        return txt
        # # print(txt)
        # # while 
        # for key in tmpDict.keys():
        #     if isinstance(tmpDict[key], dict):
        #         print(key)
        # # self.root_node.draw(g, self.root_node)
        # return txt, self.root_node.tostring(True)
        # # G = nx.DiGraph(self.root_node.tostring(True))
        # # nx.draw_networkx(g)
        # # plt.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main = Main()
        self.G = nx.DiGraph()
        self.G.add_node('class')

        self.showItem = {'showBase': True}

        self.setWindowTitle('项目类继承图')
        tool_bar = QToolBar('bar')
        self.addToolBar(tool_bar)

        self.tree = QTreeWidget()        
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('tree')
        self.tree.setHeaderHidden(True)

        box = QHBoxLayout()
        layout = QVBoxLayout()
        contaion = QWidget()

        list = ['showView', 'showItem', 'showData', 'showCtrl', 'showMgr', 'showModule', 'showOther', 'showGraph']
        t1 = QAction(QIcon(""), list[0], self)
        t1.setCheckable(True)
        t1.triggered.connect(lambda: self.onToggleTrigger(t1.isChecked(), list[0]))
        t1.setStatusTip(list[0])

        t2 = QAction(QIcon(""), list[1], self)
        t2.setCheckable(True)
        t2.triggered.connect(lambda: self.onToggleTrigger(t2.isChecked(), list[1]))
        t2.setStatusTip(list[1])

        t3 = QAction(QIcon(""), list[2], self)
        t3.setCheckable(True)
        t3.triggered.connect(lambda: self.onToggleTrigger(t3.isChecked(), list[2]))
        t3.setStatusTip(list[2])

        t4 = QAction(QIcon(""), list[3], self)
        t4.setCheckable(True)
        t4.triggered.connect(lambda: self.onToggleTrigger(t4.isChecked(), list[3]))
        t4.setStatusTip(list[3])
        tool_bar.addAction(t1)

        t5 = QAction(QIcon(""), list[4], self)
        t5.setCheckable(True)
        t5.triggered.connect(lambda: self.onToggleTrigger(t5.isChecked(), list[4]))
        t5.setStatusTip(list[4])

        t6 = QAction(QIcon(""), list[5], self)
        t6.setCheckable(True)
        t6.triggered.connect(lambda: self.onToggleTrigger(t6.isChecked(), list[5]))
        t6.setStatusTip(list[5])

        t7 = QAction(QIcon(""), list[6], self)
        t7.setCheckable(True)
        t7.triggered.connect(lambda: self.onToggleTrigger(t7.isChecked(), list[6]))
        t7.setStatusTip(list[6])

        t8 = QAction(QIcon(""), list[7], self)
        t8.setCheckable(True)
        t8.triggered.connect(lambda: self.onToggleTrigger(t8.isChecked(), list[7]))
        t8.setStatusTip(list[7])

        tool_bar.addAction(t1)
        tool_bar.addAction(t2)
        tool_bar.addAction(t3)
        tool_bar.addAction(t4)
        tool_bar.addAction(t5)
        tool_bar.addAction(t6)
        tool_bar.addAction(t7)
        tool_bar.addAction(t8)

        layout.addLayout(box)

        btn = QPushButton("开始解析")
        btn.clicked.connect(self.onStartClick)
        layout.addWidget(btn)

        layout.addWidget(self.tree)
        # self.label = QTextBrowser()
        # layout.addWidget(self.label)

        contaion.setLayout(layout)
        self.setCentralWidget(contaion)
    
    def onToggleTrigger(self, checked, name):
        self.showItem[name] = checked

    def onStartClick(self):
        self.G.clear()
        self.main.read_file(self.showItem)
        self.main.parse_node()
        self.tree.clear()
        self.tree_root = QTreeWidgetItem(self.tree)
        self.tree_root.setText(0, self.main.root_node.name)
        txt = self.main.drow_map(self.G, self.tree_root)

        # self.label.setText(txt)
        # pos = nx.multipartite_layout(self.G)
        if self.showItem[show_graph]:
            plt.figure(figsize=(10, 10))
            nx.draw_networkx(self.G, None, True)
            plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


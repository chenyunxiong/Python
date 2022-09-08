import json
import os
import glob
from posixpath import basename
import re
import networkx as nx
import matplotlib.pyplot as plt

# path = "E:\Projects\Python\lua_analysis\\"
path = 'C:\Project\gof\gof_client\Assets\Lua\\'
show_view = False
show_item = False
show_data = False
show_ctrl = False
show_mgr = False
show_base = True
show_module = True
show_other = True


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

    root_name_list = []

    def check_show_item(self, subName, parentName = None):
        if subName.endswith("Base"):
            return show_base
        if subName.endswith("Module"):
            return show_base
        if (subName.endswith("View") or subName.endswith("Panel")):
            return show_view
        if subName.endswith("Item"):
            return show_item
        if subName.endswith("Ctrl"):
            return show_ctrl
        if subName.endswith("Data"):
            return show_data
        if subName.endswith("Mgr"):
            return show_mgr
        return show_other
    
    def read_file(self):
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

    def drow_map(self, g):
        txt = json.dumps(self.root_node.tostring(True))
        print(txt)
        pass
        # G = nx.DiGraph(self.root_node.tostring(True))

        # nx.draw_networkx(G)
        # plt.show()

if __name__ == "__main__":
    main = Main()
    G = nx.DiGraph()
    main.read_file()
    main.parse_node()
    main.drow_map(G)
    nx.draw_networkx(G)
    plt.show()

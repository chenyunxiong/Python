import json
import os
import glob
from posixpath import basename
import re
import networkx as nx
import matplotlib.pyplot as plt

path = "E:\Projects\Python\lua_analysis\\"
# path = 'C:\Project\gof\gof_client\Assets\Lua\\'

class NodeData():
    name = ''
    parent = ''

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

    def tostring(self):
        if len(self.children) > 0:
            dict = {}
            dict[self.name] = {}
            for n in self.children.values():
                dict[self.name][n.name] = n.tostring()
        else:
            dict = self.name
        return dict

    def export_as_xml(self):
        pass

class Main():
    root_node = Node('class')
    node_map = {}
    tmp_map = {}

    def add_node(self, parentName, subName):
        parentNode = self.root_node.get_node(parentName)
        if parentNode != None:
            parentNode.add_child(Node(subName))
            if self.tmp_map.__contains__(parentName):
                tmpNode = self.tmp_map[parentName]
                for n in tmpNode.children.values():
                    parentNode.add_child(n)
                del self.tmp_map[parentName]
            else:
                pass
        else:
            if not self.tmp_map.__contains__(parentName):
                parentNode = Node(parentName)
                parentNode.add_child(Node(subName))
                self.tmp_map[parentName] = parentNode
            else:
                self.tmp_map[parentName].add_child(Node(subName))

    def read_file(self):
        list = glob.glob(path+'**/*.lua', recursive=True)
        for l in list:
            with open(l, 'r', encoding='utf-8') as f:
                print('name', f.name)
                lines = f.readlines()
                for line in lines:
                    str = line
                    r_base_class = re.search(r'class\(\"(.*)\"\)', str)
                    r_base2 = re.search(r'class\(\"(.*)\", me.(.*)\)', str)
                    r_base3 = re.search(r'class\(\"(.*)\", GUIBase.(.*)\)', str)
                    if r_base_class:
                        parentName = r_base_class.group(1)
                        if not self.node_map.__contains__(parentName):
                            self.node_map[parentName] = 1
                        if not self.root_node.contain_child(parentName):
                            if self.tmp_map.__contains__(parentName):
                               n = self.tmp_map[parentName]
                               del self.tmp_map[parentName]
                               self.root_node.add_child(n)
                            else:
                                self.root_node.add_child(Node(parentName))

                    if r_base2 != None:
                        parentName = r_base2.group(2)
                        subName = r_base2.group(1)
                        if not self.tmp_map.__contains__(parentName):
                            self.tmp_map[parentName] = Node(parentName)
                        self.tmp_map[parentName].add_child(Node(subName))

                    if r_base3 != None:
                        parentName = r_base3.group(2)
                        subName = r_base3.group(1)
                        if not self.tmp_map.__contains__(parentName):
                            self.tmp_map[parentName] = Node(parentName)
                        self.tmp_map[parentName].add_child(Node(subName))    


                    keys = self.tmp_map.keys()
                    for key in keys:
                        for key2 in keys:
                            
                            pass
                        pass            


        keys = self.tmp_map.keys()
        for key in keys:
            
            pass

        # print('tmp: ', self.tmp_map)
        # print('map: ', self.node_map)
        # print('final: ', json.dumps(self.root_node.tostring()))

    def drow_map(self):
        txt = json.dumps(self.root_node.tostring())
        print(txt)
        G = nx.DiGraph(self.root_node.tostring())
        nx.draw_networkx(G)
        plt.show()

if __name__ == "__main__":
    main = Main()
    main.read_file()
    main.drow_map()
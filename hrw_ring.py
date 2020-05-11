from pickle_hash import serialize,hash_code_hex

class HRWHashing(object):

    def __init__(self,nodes):
        assert len(nodes)>0
        self.nodes = set(nodes)

    def add_node(self,node):
        self.nodes.add(node)

    def del_node(self,node):
        self.nodes.remove(node)

    def get_node(self,key):
        list_weights=[]
        for node in self.nodes:
            node_bytes = serialize(node)
            key_bytes = serialize(key)
            node_hash = hash_code_hex(node_bytes+key_bytes)
            node_hash = int(node_hash,16)
            list_weights.append((node_hash,node))
        _ , node = max(list_weights)
        return node


# Nodes = []
# for i in range(5):
#     Nodes.append(f"Node{str(i)}")
#
# hrw  = HRWHashing(Nodes)
# hrw.add_node("Node6")
# hrw.del_node(Nodes[0])
# index = 0
# for j in range(50):
#     answer = hrw.get_node(str(j))
#     if answer =="Node5":
#         index = index+1
# print(index)
import bisect
import math
from server_config import NODES
from pickle_hash import serialize, hash_code_hex

class ConsistentHashRing(object):

    def __init__(self,nodes, replication=3,virtual_node=8):
        # params :  nodes is all the server nodes , numOfKeys is the total address space of ring
        assert len(nodes)>0

        # default replication is 2, if no factor is given
        self.replication_factor = replication

        # default virtual node are 8, if no factor is given
        self.virtual_node = virtual_node

        # node_location is the list with address of all the node location on the ring
        self.node_location = []

        # nodes is mapping between the node location to the actual address of the server
        self.nodes = {}
        self.numOfKeys = int(math.pow(2,32)-1)

        # node count is only for testing how evenly the distribution is being done for each node location
        self.node_count = {}
        for node in nodes:
            self.add_node(node)

    # add a new node and add its location to the list / also create virtual node for each node
    def add_node(self, node):
        node_bytes = serialize(node)
        node_bytes = str(hash_code_hex(node_bytes))

        # creating the virtual nodes for each node , params : node details and number of virtual nodes to be made
        listOfVirtualNodes = self.get_virtual_nodes(node_bytes)
        for vnode in listOfVirtualNodes:
            name_bytes = serialize(vnode)
            node_hash = str(hash_code_hex(name_bytes))
            node_hash = int(node_hash,16) % self.numOfKeys
            if node_hash in self.node_location:
                raise Exception("Node Already Exists")
            else:
                self.nodes[node_hash] = node
                bisect.insort(self.node_location,node_hash)
            #    print("New Node added at location : ",node_hash)
                self.node_count[node_hash] = list()

    # for a given key , returns the actual node address to process further
    def get_node(self,key_hash):
        key = int(key_hash,16) % self.numOfKeys
        if len(self.node_location)>0:
            index = bisect.bisect(self.node_location, key)
            replication_nodes = set()
            if self.replication_factor<=(len(self.nodes)/self.virtual_node):
                for i in range(self.replication_factor):
                    if index == len(self.node_location):
                        index = 0
                    node_key = self.node_location[index]
                    self.node_count[node_key].append(key)
                    replication_nodes.add(self.nodes[node_key])
                    index = index + 1
                return replication_nodes
            else:
                raise Exception("Replication Factor is greater than the physical nodes, please correct")
        else:
            raise Exception("No Node Exist, please add nodes to the ring")

    def get_virtual_nodes(self, nodename):
        listOfVirtualNodes = []
        for i in range (self.virtual_node):
            virtualNodeName = nodename+str(i)
            listOfVirtualNodes.append(virtualNodeName)
        return listOfVirtualNodes

    def del_node(self,node):
        node_bytes = serialize(node)
        node_bytes = str(hash_code_hex(node_bytes))
        listOfVirtualNodes = self.get_virtual_nodes(node_bytes)
        for vnode in listOfVirtualNodes:
            name_bytes = serialize(vnode)
            node_hash = str(hash_code_hex(name_bytes))
            node_hash = int(node_hash,16) % self.numOfKeys
            self.node_location.remove(node_hash)
            del self.nodes[node_hash]
            del self.node_count[node_hash]

    def test_printing(self):
        for node in self.node_location:
            print(f"Node location is {node}")
        print("=======================next======================")
        for key,val in self.nodes.items():
            print(f"Key is {key} and value is {val}")
        print("=======================next======================")
        for nkey,nval in self.node_count.items():
            print(f"Key is {nkey} and value is {nval}")

# chr = ConsistentHashRing(NODES)
# testing = {}
# for j in range(25):
#     chr.add_node("node%s"%str(j))
#     testing["node%s"%str(j)]=0
# print(chr.node_location)
#
# for i in range(100000):
#     name = chr.get_node(chr.get_hash(i))
#     testing[name] = testing[name] +1
#
# for node_key in chr.node_count:
#     print(len(chr.node_count[node_key]),chr.node_count[node_key])
#
# for key,value in testing.items():
#     print(f"The key is {key} and the value is {value}")
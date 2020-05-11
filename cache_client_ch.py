import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT
from consistent_hash_ring import ConsistentHashRing

BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def process(udp_clients):
    # params: for consistent hash_ring takes three arguments
    # first the nodes/servers list
    # second replication factor , default 3
    # third is number of virtual nodes required , default is 8

    REPLICATION_FACTOR = 2
    NUMBER_OF_VIRTUAL_NODES = 10

    client_ring = ConsistentHashRing(udp_clients,REPLICATION_FACTOR,NUMBER_OF_VIRTUAL_NODES)
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        list_of_nodes = client_ring.get_node(key)
        # replicating the data in multiple nodes
        replication_flag = False
        for node in list_of_nodes:
            if replication_flag:
                print("Replicating to other nodes")
            response = node.send(data_bytes)
            print(response,'\n')
            hash_codes.add(str(response.decode()))
            replication_flag=True



    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        list_of_nodes = client_ring.get_node(key)
        # for get operation iterating just once with the original node
        for node in list_of_nodes:
            response = node.send(data_bytes)
            print(response)
            break

#    Uncomment this to check the distribution of hash
#    client_ring.test_printing()


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)

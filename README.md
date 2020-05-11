# cmpe273-assignment4
CMPE 273 Assignment 4 (Spring 2020)

Assignment consisit of of two parts - HRW Hashing and Consistent Hashing

### ** Part A - HRW Hashing

- I started with the midterm code ( so no decorator and bloomfilter files in this code, it is in assignment 3 only ),  to run this part , run all the 4 servers and run the client **cache_client_hrw.py** , I have already setup the code that it uses the **hrw_ring.py** and also providing program output below.

### HRW Output 
<img src="https://github.com/Jaspreet-Singh-03/cmpe273-assignment3/blob/master/Program%20Outputs/Test%20Output.jpg" height="800">

### ** Part B - HRW Hashing

- Similarly, I have already setup everything and start by running all the 4 servers and then run the client **cache_client_ch.py** ,  it uses the **consistent_hash_ring.py** , I have also written comment in code if you want tweak anything , the hash ring requires 3 parameters 
- 1 : All the physical nodes/servers list/objects. 
- 2 : Replication Factor ( i have used replication of 2 in sample output below , default value is 3 if nothing is provided with max limit equal to number of physical nodes present ) 
- 3 : Number of Virtual Nodes to be made for each Physical node ( i am using 10 virtual nodes , default value is 8 if nothing is provided)  and also providing program output below.

### Consistent Hash Output 
<img src="https://github.com/Jaspreet-Singh-03/cmpe273-assignment3/blob/master/Program%20Outputs/Client%20Output.jpg" height="800">



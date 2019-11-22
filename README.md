# FogOS

## How to run
If you want to generate a new random batch of input and then run the code
```
./run.sh
```
If you want to just run the code on current input files
```
python algo2019_interface.py
```

## Changes in code [2019]
## New input generation to include content **ID** and **Delay**
### generate_with_contentid.py
Code for generating input files to algo

Generated files: 
+ substrate_network.txt
+ virtual_network_requests.txt

### substrate_network.txt
Input file including substrate network information with N nodes
+ Line 1 -> space-separated node ids
+ Line 2 -> space-separated cpu values 
+ Line 3 -> Empty line seperating information with content ids 
+ Next N (number of nodes) lines -> space-separated content id. 1 line per node 
+ Next Line -> Empty line seperating content ids with bandwith matrix
+ Next N (number of nodes) lines -> Matrix of bandwith values

### virtual_network_requests.txt
Input file which includes information of N virtual network requests
This file contains 2 types of VNR 

Format for each VNR
+ Line 1 -> VNR ID
+ Line 2 -> space-separated node ids
+ Line 3 -> space-separated cpu values 
+ Line 4 -> space-separated maxhop values 
+ Line 5 -> space-separated cid values 
+ Next N (number of nodes) lines -> Matrix of bandwith values
+ Line N + 5 -> space-separated node ids (for delay)
+ Line N + 6 -> space-separated cpu values 
+ Line N + 7 -> space-separated maxhop values 
+ Line N + 8 -> space-separated cid values 
+ Next N2 (number of nodes with delay) lines -> Matrix of bandwith values

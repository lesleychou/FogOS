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
### `generate_with_contentid.py`
Code for generating input files to algo

Generated files: 
+ substrate_network.txt
+ virtual_network_requests.txt

### `substrate.txt`
Input file including substrate network information with N nodes
+ Line 1 -> space-separated node ids
+ Line 2 -> space-separated cpu values 
+ Line 3 -> Empty line seperating information with content ids 
+ Next N (number of nodes) lines -> space-separated content id. 1 line per node 
+ Next Line -> Empty line seperating content ids with bandwith matrix
+ Next N (number of nodes) lines -> Matrix of bandwith values

### `virtual_network_requests.txt`
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

## Reading / Parsing Input data
### `read_input_from_file.py` : `get_all_input()`
This function reads `substrate.txt` and returns 4 variables  in this format:
```
   asn = [
      [70, 40, 60, 100, 80, 40, 60, 60, 60],  # CPU values
      [                                       # CID list          
        [1, 2, 5],  
        [2, 4], 
        [3, 4], 
        [6, 7], 
        [2], 
        [2, 4], 
        [5, 7], 
        [3, 2], 
        [8, 9]
      ]
    ]

  asl = [                                     
    [0, 15, 0, 40, 0, 0, 0, 0, 0],  # BW List
    [15, 0, 15, 5, 0, 0, 0, 0, 0],
    [0, 15, 0, 0, 15, 0, 0, 0, 0],
    [40, 5, 0, 0, 40, 20, 10, 0, 0],
    [0, 0, 15, 40, 0, 0, 0, 0, 10],
    [0, 0, 0, 20, 0, 0, 0, 0, 0],
    [0, 0, 0, 10, 0, 0, 0, 10, 0],
    [0, 0, 0, 0, 0, 0, 10, 0, 10],
    [0, 0, 0, 0, 10, 0, 0, 10, 0]
  ]

  cvn = [
    [                           # VNR 1 Data: (WITHOUT delay) - ODD
      [10, 11, 8],              #   CPU
      [2, 1, 3],                #   Maxhop
      [2, 1, 3]                 #   CID
    ], [                        # VNR 1 Data: (WITH delay) - EVEN
      [10, 11, 8, 0, 0, 0],     #   CPU
      [2, 1, 3, 0, 0, 0],       #   Maxhop
      [2, 1, 3, -1, -1, -1]     #   CID
    ]
        ...
  ]

  cvl = [
    [                         # VNR 1 Data: (WITHOUT delay) - ODD
      [0, 6, 6],              #  BW matrix
      [6, 0, 0],
      [6, 0, 0]
    ], [                      # VNR 1 Data: (WITH delay) - EVEN
      [0, 0, 0, 3, 2, 0],     #  BW matrix
      [0, 0, 0, 3, 0, 0],
      [0, 0, 0, 0, 0, 2],
      [3, 3, 0, 0, 0, 0],
      [2, 0, 0, 0, 0, 2],
      [0, 0, 2, 0, 2, 0]
    ]
        ...
  ]
```

Here, we assume delay to be:
```
  delay =  [
    [              # VNR 1 Delay
      [0, 2, 3],   
      [2, 0, 0],
      [3, 0, 0]
    ]
        ...
  ]
```
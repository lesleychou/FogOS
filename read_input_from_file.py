file_sn = open("substrate_network.txt", "r")
file_vnr = open("virtual_network_requests.txt", "r")


def get_nextline_as_list(f):
  return [int(i) for i in f.readline()[:-1].strip().split(' ')]

def split_to_int(line):
  return [int(i) for i in line.strip().split(' ')]

def read_space(f):
  f.readline()

def get_sn_info():
  asn, asl = [], []
  n = len(file_sn.readline().split(' '))
  cpu = get_nextline_as_list(file_sn)

  read_space(file_sn)
  cid = []
  for i in range(n):
    cid.append(get_nextline_as_list(file_sn))

  read_space(file_sn)
  bw = []
  for i in range(n):
    bw.append(get_nextline_as_list(file_sn))

  asn = [cpu, cid]
  asl = bw

  return asn, asl

def get_vnr_info():
  cvn, cvl = [], []
  cvn_delay, cvl_delay = [], []
  read_data = file_vnr.read()

  for vnr in read_data.split("\n\n")[:-1]:
    vnr_lines = vnr.split("\n")
    node_count = len(split_to_int(vnr_lines[1]))
    cpu = split_to_int(vnr_lines[2])
    maxhop = split_to_int(vnr_lines[3])
    cid = split_to_int(vnr_lines[4])
    bw = []
    for i in range(5, node_count + 5):
      bw.append(split_to_int(vnr_lines[i]))

    cvn.append([cpu, maxhop, cid])
    cvl.append(bw)

    node_count = len(split_to_int(vnr_lines[5]))
    cpu_del = split_to_int(vnr_lines[node_count + 6])
    maxhop_del = split_to_int(vnr_lines[node_count + 7])
    cid_del = split_to_int(vnr_lines[node_count + 8])
    bw_del = []
    for i in range(node_count + 9, len(vnr_lines)):
      bw_del.append(split_to_int(vnr_lines[i]))

    cvn_delay.append([cpu_del, maxhop_del, cid_del])
    cvl_delay.append(bw_del)

  return cvn, cvl, cvn_delay, cvl_delay

def get_all_input():
  asn, asl = get_sn_info()
  cvn, cvl, cvn_delay, cvl_delay = get_vnr_info()
  return asn, asl, cvn, cvl, cvn_delay, cvl_delay

def get_dummy_asn_asl():
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
  
  return asl, asn

def get_dummy_input_without_delay():

  asl, asn = get_dummy_asn_asl()  

  cvn = [
    [                 # VNR 1 Data:
      [10, 11, 8],    #   CPU
      [2, 1, 3],      #   Maxhop
      [2, 1, 3]       #   CID
    ] , [
      [5, 4],
      [2, 1],
      [4, 5]
    ]
  ]

  cvl = [
    [              # VNR 1 Data: 
      [0, 6, 6],   #  BW matrix
      [6, 0, 0],
      [6, 0, 0]
    ], [
      [0, 10],
      [10, 0]
    ]
  ]

  return asn, asl, cvn, cvl

def get_dummy_input_with_delay():

  asl, asn = get_dummy_asn_asl()  

  cvn = [
    [                 # VNR 1 Data: (WITHOUT delay)
      [10, 11, 8],    #   CPU
      [2, 1, 3],      #   Maxhop
      [2, 1, 3]       #   CID
    ], [
      [5, 4],
      [2, 1],
      [4, 5]
    ]
  ]

  cvl = [
    [              # VNR 1 Data: (WITHOUT delay)
      [0, 6, 6],   #  BW matrix
      [6, 0, 0],
      [6, 0, 0]
    ], [
      [0, 10],
      [10, 0]
    ]
  ]

  '''
  Assumed delay
  delay =  [
    [              # VNR 1 Delay
      [0, 2, 3],   
      [2, 0, 0],
      [3, 0, 0]
    ],            # VNR 2 Delay
      [0, 5],
      [5, 0]
    ]
  ]
  '''

  cvn_delay = [
    [                           # VNR 1 Data: (WITH delay)
      [10, 11, 8, 0, 0, 0],     #   CPU
      [2, 1, 3, 0, 0, 0],       #   Maxhop
      [2, 1, 3, -1, -1, -1]     #   CID
    ], [
      [5, 4, 0, 0, 0, 0],
      [2, 1, 0, 0, 0, 0],
      [4, 5, -1, -1, -1, -1]
    ]
  ]

  cvl_delay = [
    [                       # VNR 1 Data: (WITH delay)
      [0, 0, 0, 3, 2, 0],   #  BW matrix
      [0, 0, 0, 3, 0, 0],
      [0, 0, 0, 0, 0, 2],
      [3, 3, 0, 0, 0, 0],
      [2, 0, 0, 0, 0, 2],
      [0, 0, 2, 0, 2, 0]
    ], [
      [0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 0, 2],
      [2, 0, 0, 2, 0, 0],
      [0, 0, 2, 0, 2, 0],
      [0, 0, 0, 2, 0, 2],
      [0, 2, 0, 0, 2, 0]
    ]
  ]

  return asn, asl, cvn, cvl, cvn_delay, cvl_delay



if __name__ == "__main__":
  # TESTING
  # asn, asl, cvn, cvl = get_dummy_input_without_delay()
  # print(asn, asl, cvn, cvl, sep='\n')
  # asn, asl, cvn, cvl, cvn_delay, cvl_delay = get_dummy_input_with_delay()
  # print(asn, asl, cvn, cvl, cvn_delay, cvl_delay, sep='\n')
  asn, asl, cvn, cvl, cvn_delay, cvl_delay = get_all_input()



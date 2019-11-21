import random
import itertools

def get_bw_string(node_id_list, bw_edge_dict):
  '''
  Returns a string format matrix representation of bandwith between edges
    1 2 3 ... N
  1 0 6 7 ... 1
  2 6 0 3 ... 9
  3 7 3 0 ... 7
  ....... ... .
  N 1 9 7 ... 0
  '''
  bw_str = ""
  for row in node_id_list:
    for col in node_id_list:
      bw = 0
      if (row, col) not in bw_edge_dict.keys() and (col, row) not in bw_edge_dict.keys():
        bw = 0
      elif row == col:
        bw = 0
      elif row < col:
        bw = bw_edge_dict[(row, col)]
      else:
        bw = bw_edge_dict[(col, row)]
      bw_str = bw_str + str(bw) + " "
    bw_str = bw_str + "\n"
  return bw_str


def getString(char, count):
  string = ''
  for i in range(count):
    string = string + char + ' '
  return string
 
MAX_NODE_ID = 26
MAX_CONTENT_ID = 20
MAX_CONTENT_ID_COUNT = 10
MIN_CPU = 5000
MAX_CPU = 6000
MIN_BANDWIDTH = 10
MAX_BANDWIDTH = 50

SN_CPU = 0
SN_CID = 1

# Add a seed for constant random generation
random.seed(0)

'''
Creates dictionary of substrate network
  { 
    nodeid_1: [cpu, cid],
    nodeid_2: [cpu, cid],
    ... 
  }
'''
substrate_network = {}
node_id_list = []
all_cid  = []
for nodeid in range(1, MAX_NODE_ID+1):
  cpu = 1000
  # cpu = random.randint(MIN_CPU, MAX_CPU)
  cid_count = random.randint(1, MAX_CONTENT_ID_COUNT)
  cid = random.sample(range(MAX_CONTENT_ID), cid_count)
  all_cid = all_cid + cid
  substrate_network[nodeid] = [cpu, cid]
  node_id_list.append(nodeid)

all_cid = list(set(all_cid))

'''
Creates dictionary of bandwidth for substrate network in edge list format
  {
    (nodeid_x, node_id_y): bw,  
    (nodeid_x, node_id_y): bw,  
    ... 
  }
'''
sn_bw_edge = list(itertools.combinations(node_id_list, 2))
sn_bw_edge_dict = dict(list(map(lambda x: ((x[0], x[1]), random.randint(MIN_BANDWIDTH, MAX_BANDWIDTH)), sn_bw_edge)))

# Create string of node_id, cpu and bandwith for easier writing to file
cpu_str = ""
for nodeid, info in substrate_network.items():
  cpu_str = cpu_str + str(info[SN_CPU]) + " "

bw_str = get_bw_string(node_id_list, sn_bw_edge_dict)

# Write to file: Substrate Network
# Line 1 -> space-separated node ids
# Line 2 -> space-separated cpu values 
file_sn = open("substrate_network.txt", "w")
file_sn.write(str(node_id_list).strip("[]").replace(',', '') + "\n")
file_sn.write(cpu_str.strip() + "\n\n")

# Line 3 -> Empty line seperating information with content ids 
# Next N (number of nodes) lines -> space-separated content id. 1 line per node 
for nodeid, info in substrate_network.items():
  file_sn.write(" ".join(map(str, info[SN_CID])) + "\n")

# Next Line -> Empty line seperating content ids with bandwith matrix
# Next N (number of nodes) lines -> Matrix of bandwith values
file_sn.write("\n")
file_sn.write(bw_str)

VNR_COUNT = 50
MIN_DELAY = 1
MAX_DELAY = 5
MIN_MAXHOP = 1
MAX_MAXHOP = 10
VNR_MIN_CPU = 1
VNR_MAX_CPU = 50

vnr = []
file_vnr = open("virtual_network_requests.txt", "w")
# Create values for Virtual Network Requests (VNR)
for vnr_id in range(1, VNR_COUNT+1):
  node_count = random.randint(2, MAX_NODE_ID/2)
  # request_node_id_list = sorted(random.sample(node_id_list, node_count))
  request_node_id_list = [i for i in range(1, node_count+1)]
  
  # cpu_str, delay_str, maxhop_str, cid_str = "", "", "", ""
  cpu_str, maxhop_str, cid_str = "", "", ""
  for node_id in request_node_id_list:
    info = substrate_network[node_id]
    cpu = random.randint(VNR_MIN_CPU, VNR_MAX_CPU)
    # delay = random.randint(MIN_DELAY, MAX_DELAY)
    maxhop = random.randint(MIN_MAXHOP, MAX_MAXHOP)
    cid = random.sample(all_cid, 1)[0]
    
    cpu_str = cpu_str + str(cpu) + " "
    # delay_str = delay_str + str(delay) + " "
    maxhop_str = maxhop_str + str(maxhop) + " "
    cid_str = cid_str + str(cid) + " "

  file_vnr.write(str(vnr_id) + "\n")
  file_vnr.write(str(request_node_id_list).strip("[]").replace(',', '') + "\n")
  file_vnr.write(cpu_str.strip() + "\n")
  file_vnr.write(maxhop_str.strip() + "\n")
  file_vnr.write(cid_str.strip() + "\n")
  file_vnr.write(bw_str.strip() + "\n")

  delay_edge = list(itertools.combinations(request_node_id_list, 2))
  delay_edge_dict = dict(list(map(lambda x: ((x[0], x[1]), random.randint(MIN_DELAY, MAX_DELAY)), delay_edge)))

  bw_edge = list(itertools.combinations(request_node_id_list, 2))
  bw_edge_dict = dict(list(map(lambda x: ((x[0], x[1]), random.randint(MAX_DELAY, sn_bw_edge_dict[x])), bw_edge)))

  bw_edge_dict_with_delay = bw_edge_dict.copy()
  for key, bw in bw_edge_dict.items():
    delay = delay_edge_dict[key]
    if delay > 1:
      new_delay = int(bw/delay)
      num_new_nodes = int(bw/new_delay)
      bw_edge_dict_with_delay[key] = 0
      node_a, node_b = key
      if num_new_nodes == 1:
        node_new = node_count + 1
        bw_edge_dict_with_delay[(node_a, node_new)] = new_delay
        bw_edge_dict_with_delay[(node_b, node_new)] = new_delay
        node_count = node_count + 1
      else:
        for i in range(num_new_nodes):
          node_new = node_count + 1
          if i == 1:
            # First node    
            bw_edge_dict_with_delay[(node_a, node_new)] = new_delay
            bw_edge_dict_with_delay[(node_new, node_new + 1)] = new_delay
          elif i == num_new_nodes-1:
            # Last nodes
            bw_edge_dict_with_delay[(node_b, node_new)] = new_delay
          else:
            # In-between nodes
            bw_edge_dict_with_delay[(node_new, node_new + 1)] = new_delay
          node_count = node_count + 1

  added_node_count = node_count - len(request_node_id_list)
  
  cpu_str = cpu_str + getString('0', added_node_count)
  maxhop_str = maxhop_str +  getString('0', added_node_count)
  cid_str = cid_str +  getString('-1', added_node_count)

  bw_str = get_bw_string(request_node_id_list, bw_edge_dict)

  request_node_id_list = [i for i in range(1, node_count+1)]
  # print(node_count)
  # print(bw_edge_dict_with_delay)
  # print(request_node_id_list)
  bw_str_delay = get_bw_string(request_node_id_list, bw_edge_dict_with_delay)

  '''
  Write to file: ith VNR
    Line 1 -> VNR ID
    Line 2 -> space-separated node ids
    Line 3 -> space-separated cpu values 
    Line 4 -> space-separated maxhop values 
    Line 5 -> space-separated cid values 
    Next N (number of nodes) lines -> Matrix of bandwith values (without delay)
    Next N (number of nodes) lines -> Matrix of bandwith values (with delay)
  '''
  file_vnr.write(str(request_node_id_list).strip("[]").replace(',', '') + "\n")
  file_vnr.write(cpu_str.strip() + "\n")
  # file_vnr.write(delay_str.strip() + "\n")
  file_vnr.write(maxhop_str.strip() + "\n")
  file_vnr.write(cid_str.strip() + "\n")
  file_vnr.write(bw_str_delay.strip() + "\n\n")

  





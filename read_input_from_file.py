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
  read_data = file_vnr.read()

  flag = 1
  cpu, delay, maxhop, cid, bw = [], [], [], [], []
  for line in read_data.split("\n"):
    if line == "":
      if flag != 1:
        cvn.append([cpu, delay, maxhop, cid])
        cvl.append(bw)
        bw = []
      flag = 1
      continue
    elif flag == 3:
      cpu = split_to_int(line)
    elif flag == 4:
      delay = split_to_int(line)
    elif flag == 5:
      maxhop = split_to_int(line)
    elif flag == 6:
      cid = split_to_int(line)
    elif flag > 6: 
      bw.append(split_to_int(line))
    flag = flag + 1
     
  return cvn, cvl

def get_all_input():
  asn, asl = get_sn_info()
  cvn, cvl = get_vnr_info()
  print(cvl)
  return asn, asl, cvn, cvl

get_all_input()

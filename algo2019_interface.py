import networkx as nx
import matplotlib.pyplot as plt
import string
from collections import deque
from itertools import islice
from read_input_from_file import get_all_input

def GenerateVN_Nodes(network, node_attributes):
    for node_index in range(len(node_attributes[0])):
        network.add_node(alphabet_dict[node_index + 1], cpu=node_attributes[0][node_index],
                         maxhop=node_attributes[1][node_index], content=node_attributes[2][node_index])

def GenerateSN_Nodes(network, node_attributes):
    for node_index in range(len(node_attributes[0])):
        network.add_node(alphabet_dict[node_index + 1], cpu=node_attributes[0][node_index],
                         content=node_attributes[1][node_index])


def GenerateEdges(network, edge_attributes):
    for row in range(len(edge_attributes)):
        for column in range(len(edge_attributes[0])):
            if edge_attributes[row][column] > 0:
                network.add_edge(alphabet_dict[row + 1], alphabet_dict[column + 1], bw=edge_attributes[row][column])

def GetRevenue(vnr_list):
    for vnr_index in range(len(vnr_list)):
        revenue_components = []
        for node in vnr_list[vnr_index].nodes():
            revenue_components.append(vnr_list[vnr_index].nodes[node]['cpu'])  # change something here?????
            revenue_components.append(vnr_list[vnr_index].nodes[node]['maxhop'])
            revenue_components.append(vnr_list[vnr_index].nodes[node]['content'])

        for edge in vnr_list[vnr_index].edges():
            revenue_components.append(vnr_list[vnr_index].edges[edge]['bw'])
        vnr_list[vnr_index] = (vnr_list[vnr_index], sum(revenue_components))

    vnr_list.sort(key=lambda x:x[1], reverse=True)


def GetAvailableNodes(sn, maximum_cpu, vnr_list):
    match_SN_nodes = []
    for vnr in vnr_list:
        for node1 in vnr[0].nodes():
            temp = []
            for node in sn.nodes():
                # if cid == -1 then it can map to all the sn nodes
                if vnr[0].nodes[node1]['content'] == -1:
                    temp.append(node)
                # otherwise, match as below
                elif vnr[0].nodes[node1]['content'] in sn.nodes[node]['content']:
                    temp.append(node)
            match_SN_nodes.append(temp)

    possible_sn_nodes = []
    for node in sn.nodes():
        if sn.nodes[node]['cpu'] >= maximum_cpu:
            possible_sn_nodes.append(node)

    rest_sn_nodes = []
    for temp_i in match_SN_nodes:
        sn_nodes_i = list(set(temp_i) & set(possible_sn_nodes))
        rest_sn_nodes.append(sn_nodes_i)

    return rest_sn_nodes


def GetMaxAvailableResources(sn, sn_subset):
    for node_index in range(len(sn_subset)):
        max_available_resources = 0
        for edge in sn.edges(sn_subset[node_index]):
            max_available_resources += sn.nodes[sn_subset[node_index]]['cpu'] * sn.edges[edge]['bw']
        sn_subset[node_index] = (sn_subset[node_index], max_available_resources)

    sn_subset.sort(key=lambda x:x[1], reverse=True)

def SortVnrNodes(vnr):
    cpu = []
    for node in vnr.nodes():
        cpu.append(vnr.nodes[node]['cpu'])
    if cpu[1:] == cpu[:-1]:
        return sorted(vnr.nodes(data=True))
    else:
        return sorted(vnr.nodes(data=True), key=lambda x: x[1]['cpu'], reverse=True)

def AddNodeMapping(node_mapping_list, vnr_id, vnr_node, sn_node):
    node_mapping_list.append((vnr_id, vnr_node, sn_node))

def SubtractCpuResource(sn, sn_node, vnr, vnr_node):
    sn.nodes[sn_node]['cpu'] -= vnr.nodes[vnr_node]['cpu']

def ReturnCpuResource(sn, vnr, node_mapping):
    sn.nodes[node_mapping[2]]['cpu'] += vnr.nodes[node_mapping[1]]['cpu']

def RemoveNodeMapping(sn, vnr, node_mapping, node_mapping_list):
    ReturnCpuResource(sn, vnr, node_mapping)
    print(node_mapping)
    node_mapping_list.remove(node_mapping)

def AddEdgeMapping(edge_mapping_list, vnr_id, vnr_edge, sn_path):
    edge_mapping_list.append((vnr_id, vnr_edge, sn_path))

def SubtractBwResource(sn, sn_edge, vnr, vnr_edge):
    sn.edges[sn_edge]['bw'] -= vnr.edges[vnr_edge]['bw']

def ReturnBwResource(sn, sn_edge, vnr, vnr_edge):
    sn.edges[sn_edge]['bw'] += vnr.edges[vnr_edge]['bw']

def GetSnNodeMapping(node_mapping_list, vnr_id, vnr_node):
    with_vnr_id = list(filter(lambda x: x[0] == vnr_id, node_mapping_list))
    with_sn_node = list(filter(lambda x: x[1] == vnr_node, with_vnr_id))

    return with_sn_node[0][2]

def GreedyNodeMapping(sn, vnr_list, node_mapping_list, request_queue):
    successful_node_mapping = []
    for index, vnr in enumerate(vnr_list):
        print("Mapping vnr ", index)
        maximum_cpu = max(vnr[0].nodes(data=True), key=lambda x: x[1]['cpu'])[1]['cpu']
        rest_sn_nodes = GetAvailableNodes(sn, maximum_cpu, vnr_list)

        # merge the list
        MomList = rest_sn_nodes
        sn_subset = []
        for sublist in MomList:
            for item in sublist:
                sn_subset.append(item)

        possible_sn_nodes = list(set(sn_subset))
        GetMaxAvailableResources(sn, possible_sn_nodes)

        # change the possible_sn_nodes into a dict
        cpus = {}
        for node in possible_sn_nodes:
            letter, cpu = node
            cpus[letter] = cpu

        enough_resources = True
        for x in rest_sn_nodes:
            if len(x) == 0:
                print("Not enough SN resources")
                enough_resources = False

        if not enough_resources: break

        # sort the rest_sn_nodes by the cpu value
        sort_sn_nodes = []
        for a in rest_sn_nodes:
            sort_sn_nodes.append(sorted(a, key=lambda letter: cpus[letter]))

        if vnr[0].number_of_nodes() > len(possible_sn_nodes):
            request_queue.append(vnr[0])
            continue

        else:
            vnr[0].graph['node_mapping_status'] = 1

            sorted_vnr_nodes = SortVnrNodes(vnr[0])
            for node in sorted_vnr_nodes:
                selected_sn_node = sort_sn_nodes.pop(0)
                AddNodeMapping(node_mapping_list, vnr[0].graph['id'], node[0], selected_sn_node[0])
                SubtractCpuResource(sn, selected_sn_node[0], vnr[0], node[0])

        if vnr[0].graph['node_mapping_status'] == 1:
            successful_node_mapping.append(vnr[0])

    return (successful_node_mapping)

def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

def UnsplittableLinkMapping(sn, vnr_list, node_mapping_list, edge_mapping_list, request_queue):
    for vnr in vnr_list:
        selected_paths = []
        for edge in sorted(vnr[0].edges()):
            sn_node1 = GetSnNodeMapping(node_mapping_list, vnr[0].graph['id'], edge[0])
            sn_node2 = GetSnNodeMapping(node_mapping_list, vnr[0].graph['id'], edge[1])
            for path in k_shortest_paths(sn, sn_node1, sn_node2, 100):
                edge_selected = 0
                for chosen_path in selected_paths:
                    for chosen_path_index in range(len(chosen_path)-1):
                        for edge_index in range(len(path)-1):
                            if (path[edge_index] == chosen_path[chosen_path_index] and path[edge_index+1] == chosen_path[chosen_path_index+1]) or (path[edge_index] == chosen_path[chosen_path_index+1] and path[edge_index+1] == chosen_path[chosen_path_index]):
                                edge_selected = 1
                if edge_selected == 0:
                    to_map = 1
                    for edge_index in range(len(path)-1):
                        if vnr[0].edges[edge]['bw'] > sn.edges[path[edge_index], path[edge_index+1]]['bw']:
                            to_map = -1
                            break
                if to_map == 1:
                    selected_paths.append(path)
                    break
        if (len(selected_paths) < vnr[0].number_of_edges()):
            for node_mapping in list(filter(lambda x: x[0] == vnr[0].graph['id'], node_mapping_list)):
                RemoveNodeMapping(sn, vnr[0], node_mapping, node_mapping_list)
            request_queue.append(vnr[0])
        else:
            vnr[0].graph['edge_mapping_status'] = 1
            for edge in sorted(vnr[0].edges()):
                path = selected_paths.pop(0)
                AddEdgeMapping(edge_mapping_list, vnr[0].graph['id'], edge, tuple(path))
                for edge_index in range(len(path)-1):
                    SubtractBwResource(sn, (path[edge_index], path[edge_index+1]), vnr[0], edge)


def Plotting(network):
    # Hard coded position just for illustrative purposes
    #pos = { 'A': (10,20), 'B': (30, 30), 'C': (40,30), 'D': (30,20), 'E': (50,20), 'F': (20,10), 'G': (30,10), 'H': (40,10), 'I': (50,10)}
    pos = nx.spring_layout(network, scale=2)
    nx.draw_networkx_nodes(network, pos, nodelist=network.nodes(), node_color='b')
    nx.draw_networkx_edges(network, pos, nodelist=network.edges())
    network_node_labels = nx.get_node_attributes(network,"cpu")
    network_edge_labels = nx.get_edge_attributes(network,"bw")
    nx.draw_networkx_labels(network, pos, labels=network_node_labels)
    nx.draw_networkx_edge_labels(network, pos, with_labels=True, edge_labels=network_edge_labels)


# Substrate Network Input and Virtual Network Requests
asn, asl, cvn, cvl = get_all_input()

# # For lettering purposes
# alphabet_dict = dict(zip(range(1, len(asl)+1), string.ascii_uppercase))
# # For large SN
alphabet_dict = dict(zip(range(1,len(asl)+1), map(str, range(1000 + 1))))

# # Graph for Substrate Network
sn = nx.Graph()
GenerateSN_Nodes(sn, asn)
GenerateEdges(sn, asl)

sn_d = nx.Graph()
GenerateSN_Nodes(sn_d, asn)
GenerateEdges(sn_d, asl)


vnr_graph_nodelay_list = []
for vnr_index in range(len(cvn)):
    vnr_graph_nodelay_list.append(nx.Graph(id=vnr_index+1, node_mapping_status=0, edge_mapping_status=0, splittable=0))
    GenerateVN_Nodes(vnr_graph_nodelay_list[vnr_index], cvn[vnr_index])
    GenerateEdges(vnr_graph_nodelay_list[vnr_index], cvl[vnr_index])

vnr_graph_delay_list = []
for vnr_index in range(len(cvn_delay)):
    vnr_graph_delay_list.append(nx.Graph(id=vnr_index+1, node_mapping_status=0, edge_mapping_status=0, splittable=0))
    GenerateVN_Nodes(vnr_graph_delay_list[vnr_index], cvn_delay[vnr_index])
    GenerateEdges(vnr_graph_delay_list[vnr_index], cvl_delay[vnr_index])


node_mapping_list = []
edge_mapping_list = []
request_queue = deque()
node_mapping_list_d = []
edge_mapping_list_d = []
request_queue_d = deque()

GetRevenue(vnr_graph_nodelay_list)
GetRevenue(vnr_graph_delay_list)

# Greedy Node Mapping
successful_node_mapping = GreedyNodeMapping(sn, vnr_graph_nodelay_list, node_mapping_list, request_queue)
successful_node_mapping_d = GreedyNodeMapping(sn_d, vnr_graph_delay_list, node_mapping_list_d, request_queue_d)

# k-Shortest Path Link Mapping: no delay
unsplittable_vnr = []
splittable_vnr = []

for vnr in successful_node_mapping:
    if vnr.graph['splittable'] == 0:
        unsplittable_vnr.append(vnr)
    else:
        splittable_vnr.append(vnr)

GetRevenue(unsplittable_vnr)
GetRevenue(splittable_vnr)
UnsplittableLinkMapping(sn, unsplittable_vnr, node_mapping_list, edge_mapping_list, request_queue)

# k-Shortest Path Link Mapping: delay
unsplittable_vnr_d = []
splittable_vnr_d = []

for vnr in successful_node_mapping_d:
    if vnr.graph['splittable'] == 0:
        unsplittable_vnr_d.append(vnr)
    else:
        splittable_vnr_d.append(vnr)

GetRevenue(unsplittable_vnr_d)
GetRevenue(splittable_vnr_d)
UnsplittableLinkMapping(sn_d, unsplittable_vnr_d, node_mapping_list_d, edge_mapping_list_d, request_queue_d)

# Writing to Output File
output_file = open('results.txt', 'w+')
out = open('results_original_arrangement.txt', 'w+')
accepted_count = 0
results = []
for index, vnr in enumerate(vnr_graph_nodelay_list):
    # for vnd in vnr_graph_delay_list:
    vnd = vnr_graph_delay_list[index]
    if vnr[0].graph['node_mapping_status'] == 1 and vnr[0].graph['edge_mapping_status'] == 1 or \
            vnd[0].graph['node_mapping_status'] == 1 and vnd[0].graph['edge_mapping_status'] == 1:
        results.append((vnr[0].graph['id'], "Accepted"))
        out.write("Result " + str(vnr[0].graph['id']) + ": Accepted\n")
        accepted_count += 1
    else:
        results.append((vnr[0].graph['id'], "Rejected"))
        out.write("Result " + str(vnr[0].graph['id']) + ": Rejected\n")

for item in sorted(results, key=lambda x:x[0]):
    output_file.write("Result " + str(item[0]) + ": " + item[1] + "\n")

output_file.write("Acceptance Ratio: " + str(accepted_count/len(vnr_graph_delay_list)*100) + "%")
out.write("Acceptance Ratio: " + str(accepted_count/len(vnr_graph_delay_list)*100) + "%")
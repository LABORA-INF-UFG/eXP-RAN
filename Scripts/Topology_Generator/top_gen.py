# -*- coding: utf-8 -*-
import json
import math
import random
import argparse
import networkx as nx

class Node:

	def __init__ (self, nodeNumber, nodeType):
		self.nodeNumber = nodeNumber
		self.nodeType = nodeType

	def add_vm (self, vm):
		if not hasattr(self,'vms'):
			self.vms = []
		self.vms.append(vm)

class VM:

	def __init__ (self, vmNumber, cpu, ram):
		self.vmNumber = vmNumber
		self.cpu = cpu
		self.ram = ram

class Link:

	def __init__ (self, linkNumber, from_node, to_node, capacity, delay):
		self.linkNumber = linkNumber
		self.from_node = from_node
		self.to_node = to_node
		self.delay = delay
		self.capacity = capacity

def serialize (obj):
	return obj.__dict__

def gen_vms_profile ():

	vms_profile = []

	processor = [1, 2, 4, 8]
	memory = [1024, 2048, 4096, 8192]

	for vcpus in processor:
		for ram in memory:
			vms_profile.append({'cpu': vcpus, 'ram': ram})

	return vms_profile

def gen_link_profile ():

	links_profile = []

	mm_wave_bw = [0.9, 1.25, 1.5, 2, 3, 4, 8]
	micro_wave_bw = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.25, 1.5, 2]
	copper_bw = [1, 10, 40]
	smf_fiber_1310_bw = [1, 10, 40, 100]
	smf_fiber_1550_bw = [1, 10, 40, 100]
	tbe_bw = [200, 400]

	mm_wave_delay = range(1, 21)
	micro_wave_delay = range(1, 101)
	copper_delay = []

	n = 0.05
	for i in range(50):
		copper_delay.append(n + (i * 0.02))

	smf_fiber_1310_delay = range(1, 201)
	smf_fiber_1550_delay = range(1, 351)
	tbe_delay = range (1, 51)

	for bw in mm_wave_bw:
		for delay in mm_wave_delay:
			dist = delay * 0.3
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

	for bw in micro_wave_bw:
		for delay in micro_wave_delay:
			dist = delay * 0.3
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

	for bw in copper_bw:

		if(bw == 1):

			for delay in copper_delay:
				dist = delay * 0.02
				links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

		elif(bw == 10):

			delay = 0.275
			dist = 0.055
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

		else:

			delay = 0.15
			dist = 0.03
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

	for bw in smf_fiber_1310_bw:

		if(bw == 1):

			for delay in smf_fiber_1310_delay:
				dist = delay * 0.2
				links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

		else:

			delay = 50
			dist = 10
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

	for bw in smf_fiber_1550_bw:

		if(bw == 1):

			for delay in smf_fiber_1550_delay:
				dist = delay * 0.2
				links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

		else:

			delay = 200
			dist = 40
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

	for bw in tbe_bw:
		for delay in tbe_delay:
			dist = delay * 0.2
			links_profile.append({'delay': delay, 'bw': bw, 'dist': dist})

	return links_profile

def draw_nodes (graph, vms_profile):

	node_list = []
	node_type = ["MECServer", "BaseStation", "Forwarding"]
	nodeCount = 1
	vmCount = 1
	num_nodes = nx.number_of_nodes(graph)
	number_mec = int(round(num_nodes * 0.05))
	number_Base_Station = int(round(num_nodes * 0.3))
	number_forwarding = num_nodes - number_Base_Station - number_mec
	graph_nodes = list(graph.nodes)

	for i in range(number_mec):

		choice = random.choice(graph_nodes)
		graph_nodes.remove(choice)
		node = (Node(nodeCount, 'MECServer'))
		nodeCount += 1

		numberVMs = random.randint(1, 10)

		for j in range (numberVMs):
			profile = random.choice(vms_profile)
			node.add_vm(VM(vmCount, profile['cpu'], profile['ram']))
			vmCount += 1

		node_list.append(node)
		
	for i in range(number_Base_Station):

		choice = random.choice(graph_nodes)
		graph_nodes.remove(choice)

		node = (Node(nodeCount, 'BaseStation'))
		node.add_vm(VM(vmCount, 1, 1024))
		node_list.append(node)
		nodeCount += 1
		vmCount += 1

	for i in range(number_forwarding):
		choice = random.choice(graph_nodes)
		graph_nodes.remove(choice)
		node_list.append(Node(nodeCount, 'Forwarding'))
		nodeCount += 1

	return node_list

def closest_dist(links_profile, distance):

	aux = []
	min_diff = 1000000
	closest_dist = -1

	for link in links_profile:

		if abs(link['dist'] - distance) < min_diff:
			min_diff = abs(link['dist'] - distance)
			closest_dist = link['dist']

	return closest_dist

def draw_links (graph, links_profile, L):

	links_list = []
	nodeCount = 1
	pos = nx.get_node_attributes(graph, 'pos')

	for edge in graph.edges:
		
		x1, y1 = pos[edge[0]]
		x2, y2 = pos[edge[1]]
		distance =  math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * L

		closest = closest_dist(links_profile, distance)

		profile = random.choice([link for link in links_profile if link['dist'] == closest])

		links_list.append(Link(nodeCount, edge[0] + 1, edge[1] + 1, profile['bw'], profile['delay']))
		nodeCount += 1

	return links_list

def gen_topology(num_nodes, alpha, beta, L):
	graph = nx.waxman_graph(num_nodes, beta, alpha, L)
	
	while not nx.is_connected(graph):
		graph = nx.waxman_graph(num_nodes, beta, alpha, L)

	return graph

def save_json(node_list, links_list, user):

	topology = {"user": user, "nodes": node_list, "links": links_list}
	json_out_file = open('topology.json', 'w')
	json.dump(topology, json_out_file, default=serialize)

def generate_topology(num_nodes, alpha, beta, L, user):
	graph = gen_topology(num_nodes, alpha, beta, L)
	links_profile = gen_link_profile()
	links_list = draw_links(graph, links_profile, L)
	vms_profile = gen_vms_profile()
	node_list = draw_nodes(graph, vms_profile)
	save_json(node_list, links_list, user)

def main ():

	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", help="Your username")
	parser.add_argument("-n", "--nodes", help="Number of nodes", type=int)
	parser.add_argument("-a", "--alpha", help="Alpha Model parameter", type=float)
	parser.add_argument("-b", "--beta", help="Beta Model parameter", type=float)
	parser.add_argument("-l", "--dist", help="Maximum distance between nodes", type=float)

	args = parser.parse_args()

	generate_topology(args.nodes, args.alpha, args.beta, args.dist, args.username)

if __name__ == '__main__':
	main()
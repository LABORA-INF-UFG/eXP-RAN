import sys
import json
import math
import argparse

class VM():
  def __init__(self, id, cpu, ram):
    self.id = id
    self.cpu = cpu
    self.ram = ram
    self.containers = []

  def add_container(self, ctn):
    self.containers.append(ctn)
    self.cpu += ctn.cpu
    self.ram += ctn.ram


class Container():
  def __init__(self, id, cpu, ram):
    self.id = id
    self.cpu = cpu
    self.ram = ram

def convert_solution(user, fluidran_sol_filename, topology_filename):
	fluidran_file = open(fluidran_sol_filename, "r")
	topology_file = open(topology_filename, "r")
	fluidran_data = json.load(fluidran_file)
	topology_data = json.load(topology_file)

	infra = {}
	services = {}

	services["services"] = []
	flows_data = []

	infra["user"] = user
	infra["nodes"] = []
	infra["links"] = []

	nodes_dict = {}
	nodes_vms = {}

	link_nodes = {}
	link_nodes["linkType"] = "Nodes"
	link_nodes["Connections"] = []

	link_num = 1

	for link in topology_data["links"]:
		link_data = {
			"linkNumber": link_num,
			"fromNode": link["from_id"],
			"toNode": link["to_id"],
			"delay":  float(link["delay"]) / 1000,
			"capacity": (float(link["capacity"]) * 1000) / 20
		}

		link_nodes["Connections"].append(link_data)
		link_num += 1

	infra["links"].append(link_nodes)


	for node in (topology_data["nodes"] + topology_data["drawn_epcs"]):
		node_data = {
			"nodeNumber": node["id"],
			"nodeType": "Forwarding"
		}

		nodes_dict[int(node["id"])] = node_data

	vm_num = 1
	ctn_num = 1

	for node in topology_data["drawn_cus"]:
		node_data = {
			"nodeNumber": node["id"],
			"nodeType": "MECHost"
		}

		nodes_dict[int(node["id"])] = node_data
		nodes_dict[int(node["id"])]["vms"] = []

		nodes_vms[int(node["id"])] = VM(vm_num, 0, 0)
		vm_num += 1


	for node in topology_data["drawn_rus"]:
		node_data = {
			"nodeNumber": node["id"],
			"nodeType": "BaseStation"
		}

		nodes_dict[int(node["id"])] = node_data
		nodes_dict[int(node["id"])]["vms"] = []

		nodes_vms[int(node["id"])] = VM(vm_num, 0, 0)
		vm_num += 1



	flow_id = 1

	for flow in fluidran_data["flows"]:
		ctn_num_source = ctn_num
		ctn_num_target = ctn_num + 1
		ctn_num += 2

		fpath = []

		for seq in flow["path"]["seq"]:
			fpath.append(seq[0])

		fpath.append(flow["path"]["target"])

		flow_data = {
			"flowIdentifier": flow_id,
			"bandwidth": float(flow["value"]) / 20,
			"nodes": fpath,
			"ctnSourceNum": ctn_num_source,
			"ctnTargetNum": ctn_num_target,
		}

		flows_data.append(flow_data)

		flow_id += 1

		nodes_vms[int(flow["path"]["source"])].add_container(Container(ctn_num_source, 0.5, 512))
		nodes_vms[int(flow["path"]["target"])].add_container(Container(ctn_num_target, 0.2, 512))


	for node in topology_data["drawn_cus"]:
		vm = {
			"vmNumber": nodes_vms[int(node["id"])].id,
			"cpu": int(math.ceil(nodes_vms[int(node["id"])].cpu * 1.10)),
			"ram": int(math.ceil(nodes_vms[int(node["id"])].ram * 1.10)),
			"containers": []
		}

		for container in nodes_vms[int(node["id"])].containers:
			ctn = {
				"ctnNumber": container.id,
				"cpu": container.cpu,
				"ram": container.ram
			}

			vm["containers"].append(ctn)

		nodes_dict[int(node["id"])]["vms"].append(vm)

	for node in topology_data["drawn_rus"]:
		vm = {
			"vmNumber": nodes_vms[int(node["id"])].id,
			"cpu": int(math.ceil(nodes_vms[int(node["id"])].cpu * 1.10)),
			"ram": int(math.ceil(nodes_vms[int(node["id"])].ram * 1.10)),
			"containers": []
		}

		for container in nodes_vms[int(node["id"])].containers:
			ctn = {
				"ctnNumber": container.id,
				"cpu": container.cpu,
				"ram": container.ram
			}

			vm["containers"].append(ctn)

		nodes_dict[int(node["id"])]["vms"].append(vm)

	for node in nodes_dict:
		infra["nodes"].append(nodes_dict[node])


	services["services"].append({"flows": flows_data})

	infra_file = open("infrastructure.json", "w")
	json.dump(infra, infra_file, indent=4)
	infra_file.close()

	services_file = open("vRAN_MEC_services.json", "w")
	json.dump(services, services_file, indent=4)
	services_file.close()

def main ():

	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", help="Your username")
	parser.add_argument("-s", "--sol_file", help="Solution file")
	parser.add_argument("-t", "--top_file", help="Topology file")

	args = parser.parse_args()

	convert_solution(args.username, args.sol_file, args.top_file)

if __name__ == '__main__':
	main()
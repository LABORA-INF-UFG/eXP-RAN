# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import paramiko
import net_model
import net_controller

if __name__ == '__main__':
	pass

def serialize (obj):
	return obj.__dict__

def deploy_net_rules(emul_type, fileInfra, fileServ):

	with open(fileServ, "r") as serv_file:

		serv_data = json.load(serv_file)
		services = serv_data["services"]

		if(emul_type == "vran"):
			flow_tos = {}

		with open(fileInfra, "r") as infra_file:

			infra_data = json.load(infra_file)
			nodes = infra_data["nodes"]

			if(emul_type == "vran"):
				for i in range(len(nodes)):
					flow_tos[i] = {}
					for j in range(len(nodes)):
						flow_tos[i][j] = 0

		for service in services:

			flow_count = 0
			flows = services[0]["flows"]

			if(emul_type == "vran"):
				i = 0
				tos = 0

			for flow in flows:

				nodes = flows[flow_count]["nodes"]

				if(emul_type == "vran"):
					flow_client = nodes[0] #gen
					flow_server = nodes[-1] #recp
					bandwidth = flows[flow_count]["bandwidth"]
					flow_tos[int(flow_client)][int(flow_server)] = 4
					tos = flow_tos[int(flow_client)][int(flow_server)]

				elif(emul_type == "video"):
					flow_server = nodes[0] #gen
					flow_client = nodes[-1] #recp

				with open(fileInfra, "r") as infra_file:

					infra_data = json.load(infra_file)
					nodes = infra_data["nodes"]

					for node in nodes:

						if(emul_type == "vran"):

							if(node["nodeNumber"] == flow_client):

								vm_client = node["vms"][0]
								ctn_client = flows[flow_count]["ctnSourceNum"]
								VMclientip = '169.254.{}.{}'.format(node["nodeNumber"], vm_client["vmNumber"])

							if(node["nodeNumber"] == flow_server):

								vm_server = node["vms"][0]
								ctn_server = flows[flow_count]["ctnTargetNum"]
								VMserverip = '169.254.{}.{}'.format(node["nodeNumber"], vm_server["vmNumber"])

						elif(emul_type == "video"):

							if(node["nodeNumber"] == flow_server):

								vm_server = node["vms"][0]
								ctn_server = flows[flow_count]["ctnSourceNum"]
								VMserverip = '169.254.{}.{}'.format(node["nodeNumber"], vm_server["vmNumber"])

							if(node["nodeNumber"] == flow_client):

								vm_client = node["vms"][0]
								ctn_client = flows[flow_count]["ctnTargetNum"]
								VMclientip = '169.254.{}.{}'.format(node["nodeNumber"], vm_client["vmNumber"])

				flow_count += 1

				if(emul_type == "vran"):
					source_ip = '192.168.{}.{}'.format(vm_client["vmNumber"], ctn_client)
					target_ip = '192.168.{}.{}'.format(vm_server["vmNumber"], ctn_server)
					flow_obj = net_model.Flow_vran(int(flow_client), int(flow_server), source_ip, target_ip, flow["nodes"], bandwidth, tos)

					if tos != 4:
						net_controller.NetController.apply_rules_vran(flow_obj, net_model.network, False)
					else:
						net_controller.NetController.apply_rules_vran(flow_obj, net_model.network, True)

				elif(emul_type == "video"):
					source_ip = '192.168.{}.{}'.format(vm_server["vmNumber"], ctn_server)
					target_ip = '192.168.{}.{}'.format(vm_client["vmNumber"], ctn_client)
					flow_obj = net_model.Flow_video(int(flow_client), int(flow_server), source_ip, target_ip, flow["nodes"])
					net_controller.NetController.apply_rules_video(flow_obj, net_model.network)
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import paramiko

if __name__ == '__main__':
	pass

def serialize (obj):
	return obj.__dict__

def read_file (file):

	with open (file, "r") as myfile:
		data=myfile.read().replace('\n', '')

	return data

def deploy_services(emul_type, duration, fileInfra, fileServ, default_bwd):

	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-18]

	directory = "/home/expran/results"

	if(emul_type == "video"):
		determine_client = 1
		n_servs = 1

	with open(fileServ, "r") as serv_file:

		serv_data = json.load(serv_file)
		services = serv_data["services"]

		if(emul_type == "vran"):

			flow_tos = {}

			with open(fileInfra, "r") as infra_file:

				infra_data = json.load(infra_file)
				nodes = infra_data["nodes"]

				for i in range(len(nodes)):
					flow_tos[i] = {}
					for j in range(len(nodes)):
						flow_tos[i][j] = 0

		for service in services:

			i = 0
			flows = services[0]["flows"]
			flow_count = 0

			if(emul_type == "video"):

				trash_service_ctns = []

			for flow in flows:

				nodes = flows[flow_count]["nodes"]

				if(emul_type == "vran"):
					bandwidth = flows[flow_count]["bandwidth"]
					flow_client = nodes[0] #gen
					flow_server = nodes[-1] #recp
					flow_tos[int(flow_client)][int(flow_server)] = 4
					tos = flow_tos[int(flow_client)][int(flow_server)]

				elif(emul_type == "video"):

					if(determine_client % 2 != 0):

						nodes_pair = flows[flow_count + 1]["nodes"]
						flow_client_premium = nodes[-1]
						flow_client_trash = nodes_pair[-1]
						determine_client = 0

					else:
						determine_client = 1

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

								if(flow_client == flow_client_trash):
									trash_service_ctns.append(ctn_client)

				flow_count += 1

				if(emul_type == "vran"):

					source_ip = '192.168.{}.{}'.format(vm_client["vmNumber"], ctn_client)
					target_ip = '192.168.{}.{}'.format(vm_server["vmNumber"], ctn_server)

					# Subindo server
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMserverip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn{} sh -c "iperf -s -u -e -i 1 > server{}.txt"'.format(ctn_server, flows[i]["flowIdentifier"]))
					time.sleep(0.5)
					ssh.close()

					# Subindo client
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMclientip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn{} sh -c "iperf -c 192.168.{}.{} -u -b {}m -e --tos {} -i 1 -t {} > client{}.txt"'.format(ctn_client, vm_server["vmNumber"], ctn_server, bandwidth, tos, int(duration), flows[i]["flowIdentifier"]))
					time.sleep(0.5)
					ssh.close()
					print ("Flow {} started".format(flows[i]["flowIdentifier"]))
					i += 1

				elif(emul_type == "video"):
					source_ip = '192.168.{}.{}'.format(vm_server["vmNumber"], ctn_server)
					target_ip = '192.168.{}.{}'.format(vm_client["vmNumber"], ctn_client)

					if(flow_client == flow_client_premium): #Premium

						# Subindo client
						ssh = paramiko.SSHClient()
						ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
						ssh.connect(VMclientip, username='root', password='necos')

						ctn_int = read_file("/home/expran/expran_temp/ctn{}_interface.txt".format(ctn_client))
						stdin, stdout, stderr = ssh.exec_command('tc qdisc add dev {} root handle 1: netem delay 0.1ms && tc qdisc add dev {} parent 1: handle 2: tbf rate 1mbit burst 32kbit latency 0.01ms'.format(ctn_int, ctn_int))
						stdin, stdout, stderr = ssh.exec_command('python interface_stats_collector.py {} {}'.format(ctn_int, ctn_client))
						stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn{} sh -c \'ffmpeg -re -i "udp://{}:48550" -f mpegts image.jpg\''.format(ctn_client, target_ip))
						time.sleep(5)
						ssh.close()

						# Subindo server
						ssh = paramiko.SSHClient()
						ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
						ssh.connect(VMserverip, username='root', password='necos')
						stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn{} sh -c \'ffmpeg -re -loop 1 -i mnt/image.jpg -f mpegts udp://{}:48550\''.format(ctn_server, target_ip))
						time.sleep(1)
						ssh.close()

					elif(flow_client == flow_client_trash): #Trash

						# Subindo client
						ssh = paramiko.SSHClient()
						ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
						ssh.connect(VMclientip, username='root', password='necos')

						ctn_counter = 0

						for ctns in trash_service_ctns:

							ctn_int = read_file("/home/expran/expran_temp/ctn{}_interface.txt".format(trash_service_ctns[ctn_counter]))
							stdin, stdout, stderr = ssh.exec_command('tc qdisc del dev {} root netem'.format(ctn_int))
							stdin, stdout, stderr = ssh.exec_command('tc qdisc add dev {} root handle 1: netem delay 0.1ms && tc qdisc add dev {} parent 1: handle 2: tbf rate {}mbit burst 32kbit latency 0.01ms'.format(ctn_int, ctn_int, default_bwd))
							ctn_counter += 1

						stdin, stdout, stderr = ssh.exec_command('python interface_stats_collector.py {} {}'.format(ctn_int, ctn_client))
						stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn{} sh -c \'ffmpeg -re -i "udp://{}:48550" -f mpegts image.jpg\''.format(ctn_client, target_ip))
						time.sleep(5)
						ssh.close()

						# Subindo server
						ssh = paramiko.SSHClient()
						ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
						ssh.connect(VMserverip, username='root', password='necos')
						stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn{} sh -c \'ffmpeg -re -loop 1 -i mnt/image.jpg -f mpegts udp://{}:48550\''.format(ctn_server, target_ip))
						time.sleep(1)
						ssh.close()

					if(i % 2 != 0):
						n_servs += 1
						default_bwd = round((1.0 / n_servs), 2)
						print("Set {} deployed".format(i))
						time.sleep(int(duration))

					i += 1

			time.sleep(int(duration) + 5)
			i = 0
			flow_count = 0

			for flow in flows:

				nodes = flows[flow_count]["nodes"]

				if(emul_type == "vran"):
					flow_client = nodes[0] #gen
					flow_server = nodes[-1] #recp

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
								VMserverip = '169.254.{}.{}'.format(node["nodeNumber"], vm_server["vmNumber"])

							if(node["nodeNumber"] == flow_client):

								vm_client = node["vms"][0]
								VMclientip = '169.254.{}.{}'.format(node["nodeNumber"], vm_client["vmNumber"])

				flow_count += 1

				if(emul_type == "vran"):

					print ("Flow {} finished".format(flows[i]["flowIdentifier"]))
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMserverip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('docker cp ctn{}:/server{}.txt /root/server{}.txt'.format(ctn_server, flows[i]["flowIdentifier"], flows[i]["flowIdentifier"]))
					time.sleep(1)
					stdin, stdout, stderr = ssh.exec_command('python file_copier.py {}'.format(directory))
					ssh.close()

					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMclientip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('docker cp ctn{}:/client{}.txt /root/client{}.txt'.format(ctn_client, flows[i]["flowIdentifier"], flows[i]["flowIdentifier"]))
					time.sleep(1)
					stdin, stdout, stderr = ssh.exec_command('python file_copier.py {}'.format(directory))
					ssh.close()

					i += 1

				elif(emul_type == "video"):

					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMclientip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('python file_copier.py {}'.format(directory))
					time.sleep(3)
					ssh.close()

					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMserverip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('python file_copier.py {}'.format(directory))
					time.sleep(3)
					ssh.close()

					i += 1

	print ("Emulation finished!")
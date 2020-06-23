# -*- coding: utf-8 -*-
import os
import sys
import json
import math
import time
import random
import paramiko

if __name__ == '__main__':
	pass

def serialize (obj):
	return obj.__dict__

def deploy_infrastructure(fileADir, vcpu1, vcpu2):

	print ("Applying first network rule")

	os.system('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
	os.system('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

	with open(fileADir, "r") as json_file:

		data = json.load(json_file)
		nodes = data["nodes"]
		links = data["links"]
		user = data["user"]

		dir_path = os.path.dirname(os.path.realpath(__file__))
		dir_path = dir_path[:-20]

		os.system ("mkdir {}/{}".format(dir_path, user))

		resultsdir = '/home/expran/results'

		if(os.path.isdir(resultsdir)!= 1):
			os.system ("mkdir -m 777 {}".format(resultsdir))

		directory = "{}/{}/".format(dir_path, user)

		print ("Creating RAN Network")

		os.system("ovs-vsctl add-br br-exp-ran && ifconfig br-exp-ran 0 && ifconfig br-exp-ran 169.254.0.1/16")

		for node in nodes:

			#Creating Node switch for each Node
			os.system("ovs-vsctl add-br sw{}".format(node["nodeNumber"]))
			os.system("ifconfig sw{} up".format(node["nodeNumber"]))

			if(node["nodeType"] == "MECHost" or node["nodeType"] == "BaseStation"):

				#Creating a ToR switch for each Node
				os.system("ovs-vsctl add-br tor{}".format(node["nodeNumber"]))
				os.system("ifconfig tor{} up".format(node["nodeNumber"]))

				os.system("ip link add sw-pt{} type veth peer name tor-pt{}".format(node["nodeNumber"], node["nodeNumber"]))
			
				os.system("ifconfig sw-pt{} up".format(node["nodeNumber"]))
				os.system("ifconfig tor-pt{} up".format(node["nodeNumber"]))

				#Connecting each Node switch to each ToR switch
				os.system("ovs-vsctl add-port sw{} tor-pt{}".format(node["nodeNumber"], node["nodeNumber"]))
				os.system("ovs-vsctl add-port tor{} sw-pt{}".format(node["nodeNumber"], node["nodeNumber"]))

				vms = node["vms"]

				for vm in vms:

					#getting VM VCPUs amount
					vcpus = vm["cpu"]
					#getting VM RAM amount
					memory = vm["ram"]

					#cloning standard disk to new VM
					os.system("cp {}/XenVM/expran-disk {}{}-expdisk{}".format(dir_path, directory, user, vm["vmNumber"]))
					#cloning standard swap disk to new VM
					os.system("cp {}/XenVM/expran-swap {}{}-expswap{}".format(dir_path, directory, user, vm["vmNumber"]))
					
					#editing the cfg file for the new VM
					CPU_string = "vcpus = '2'"
					RAM_string = "memory = '2048'"
					disk_string = "disk = ['phy:/dev/vg0/expran-disk,xvda2,w','phy:/dev/vg0/expran-swap,xvda1,w',]"
					hostname_string = "name = 'expran'"
					bridge_string = "vif = ['script=vif-openvswitch, bridge=br-exp-ran']"

					file = "{}/XenVM/expran.cfg".format(dir_path)

					with open(file, "r") as old_cfg:

						with open("{}/exp{}_{}.cfg".format(directory, node["nodeNumber"], vm["vmNumber"]), "w+") as new_cfg:
							
							for line in old_cfg:

								if(line.rstrip() == CPU_string):
									new_cfg.write(line.replace(CPU_string, "vcpus = '{}'".format(vcpus)))

								elif(line.rstrip() == RAM_string):
									new_cfg.write(line.replace(RAM_string, "memory = '{}'".format(memory)))

								elif(line.rstrip() == disk_string):
									new_cfg.write(line.replace(disk_string, "disk = ['phy:{}{}-expdisk{},xvda2,w','phy:{}{}-expswap{},xvda1,w',]".format(directory, user, vm["vmNumber"], directory, user, vm["vmNumber"])))

								elif(line.rstrip() == hostname_string):
									new_cfg.write(line.replace(hostname_string, "name = '{}-exp{}'".format(user, vm["vmNumber"])))

								elif(line.rstrip() == bridge_string):
									new_cfg.write(line.replace(bridge_string, "vif = [ 'script=vif-openvswitch, bridge=br-exp-ran', 'script=vif-openvswitch,bridge=tor{}' ]".format(node["nodeNumber"])))

								else:
									new_cfg.write(line)

					old_cfg.close()
					new_cfg.close()

		print ("Setting Network Rules")

		#Creating the links between the nodes
		for link in links:

			if(link["linkType"] == "Nodes"):

				connections = link["Connections"]

				for connection in connections:

					os.system("ip link add veth{}_{} type veth peer name veth{}_{}".format(connection["fromNode"], connection["toNode"], connection["toNode"], connection["fromNode"]))
			
					os.system("ifconfig veth{}_{} up".format(connection["fromNode"], connection["toNode"]))
					os.system("ifconfig veth{}_{} up".format(connection["toNode"], connection["fromNode"]))

					os.system("ifconfig veth{}_{} mtu 1600".format(connection["fromNode"], connection["toNode"]))
					os.system("ifconfig veth{}_{} mtu 1600".format(connection["toNode"], connection["fromNode"]))

					os.system("ovs-vsctl add-port sw{} veth{}_{}".format(connection["fromNode"], connection["fromNode"], connection["toNode"]))
					os.system("ovs-vsctl add-port sw{} veth{}_{}".format(connection["toNode"], connection["toNode"], connection["fromNode"]))

		print ("Creating VMs")

		for node in nodes:

			if(node["nodeType"] == "MECHost" or node["nodeType"] == "BaseStation"):

				vms = node["vms"]

				for vm in vms:

					os.system("xl create {}exp{}_{}.cfg".format(directory, node["nodeNumber"], vm["vmNumber"]))
					time.sleep(15)

					print ("VM_{}_{} created".format(node["nodeNumber"], vm["vmNumber"]))

					VMip = '169.254.0.2'
					Node_VM = "_" + str(node["nodeNumber"]) + "_" + str(vm["vmNumber"]) + "_"

					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMip, username='root', password='necos')
					stdin, stdout, stderr = ssh.exec_command('ovs-vsctl add-br VM{}SWC && ovs-vsctl add-br VM{}SWD && ifconfig VM{}SWC 0 && ifconfig VM{}SWD 0 && python net_config.py {} {} && ifconfig VM{}SWC 169.254.{}.{}/16 && ifconfig VM{}SWD 172.16.{}.{}/16 && ovs-vsctl add-port VM{}SWC eth0 && ifconfig eth0 0 && ovs-vsctl add-port VM{}SWD eth1 && ifconfig eth1 0 && systemctl restart networking'.format(Node_VM, Node_VM, Node_VM, Node_VM, node["nodeNumber"], vm["vmNumber"], Node_VM, node["nodeNumber"], vm["vmNumber"], Node_VM, node["nodeNumber"], vm["vmNumber"], Node_VM, Node_VM))
					
					stdin, stdout, stdrr = ssh.exec_command('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
					stdin, stdout, stdrr = ssh.exec_command('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
					stdin, stdout, stdrr = ssh.exec_command('ssh-keygen -R 169.254.0.1')

					ssh.close()

		for node in nodes:

			if(node["nodeType"] == "MECHost" or node["nodeType"] == "BaseStation"):

				vms = node["vms"]

				for vm in vms:

					containers = vm["containers"]
					Node_VM = "_" + str(node["nodeNumber"]) + "_" + str(vm["vmNumber"]) + "_"

					VMip = '169.254.{}.{}'.format(node["nodeNumber"], vm["vmNumber"])
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(VMip, username='root', password='necos')
					
					for ctn in containers:

						if(ctn["ctnNumber"] == 1):

							stdin, stdout, stderr = ssh.exec_command('docker run -d -t --name=ctn{} --net=none --cpus={} --memory={}m vran'.format(ctn["ctnNumber"], vcpu1, ctn["ram"]))
							time.sleep(5)
							print ("CTN_{} created inside VM_{}_{}".format(ctn["ctnNumber"], node["nodeNumber"], vm["vmNumber"]))
							stdin, stdout, stderr = ssh.exec_command('ovs-docker add-port VM_{}_{}_SWD eth0 ctn{} --ipaddress=192.168.{}.{}/16 --gateway=192.168.0.{}'.format(node["nodeNumber"], vm["vmNumber"], ctn["ctnNumber"], vm["vmNumber"], ctn["ctnNumber"], vm["vmNumber"]))

						else:

							stdin, stdout, stderr = ssh.exec_command('docker run -d -t --name=ctn{} --net=none --cpus={} --memory={}m vran'.format(ctn["ctnNumber"], vcpu2, ctn["ram"]))
							time.sleep(5)
							print ("CTN_{} created inside VM_{}_{}".format(ctn["ctnNumber"], node["nodeNumber"], vm["vmNumber"]))
							stdin, stdout, stderr = ssh.exec_command('ovs-docker add-port VM_{}_{}_SWD eth0 ctn{} --ipaddress=192.168.{}.{}/16 --gateway=192.168.0.{}'.format(node["nodeNumber"], vm["vmNumber"], ctn["ctnNumber"], vm["vmNumber"], ctn["ctnNumber"], vm["vmNumber"]))

				ssh.close()
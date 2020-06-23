# -*- coding: utf-8 -*-

import os
import json
import time

if __name__ == '__main__':
	pass

def serialize (obj):
	return obj.__dict__

def destroy_infra(user_del, fileADir):

	print ("Destroying infrastructure...")

	with open(fileADir, "r") as json_file:

		data = json.load(json_file)
		nodes = data["nodes"]
		links = data["links"]
		user = data["user"]

		for node in nodes:

			if(node["nodeType"] == "MECHost" or node["nodeType"] == "BaseStation"):

				vms = node["vms"]

				for vm in vms:
					os.system("xl -f destroy {}-exp{} >/dev/null 2>&1".format(user, vm["vmNumber"]))

				os.system("ip link del sw-pt{} >/dev/null 2>&1".format(node["nodeNumber"]))
		   		os.system("ip link del tor-pt{} >/dev/null 2>&1".format(node["nodeNumber"]))

			os.system("ovs-vsctl del-br sw{} >/dev/null 2>&1".format(node["nodeNumber"]))
			os.system("ovs-vsctl del-br tor{} >/dev/null 2>&1".format(node["nodeNumber"]))

			for link in links:

				if(link["linkType"] == "Nodes"):

					connections = link["Connections"]

					for connection in connections:
						os.system("ip link del veth{}_{} >/dev/null 2>&1".format(connection["fromNode"], connection["toNode"]))

		time.sleep(15)

		os.system("ovs-vsctl del-br br-exp-ran >/dev/null 2>&1")
		os.system("rm -rf /home/expran/expran_temp >/dev/null 2>&1")
		os.system("rm -rf ../../{} >/dev/null 2>&1".format(user))
		os.system("rm *.pyc >/dev/null 2>&1")

		if(user_del == "y"):
			os.system("userdel expran && rm -rf /home/expran")
			print ("Infrastructure destroyed")

		elif(user_del == "n"):
			print ("Infrastructure destroyed")
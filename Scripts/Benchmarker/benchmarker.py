# -*- coding: utf-8 -*-
import os
import argparse
import infrastructure_manager as infra
import service_manager as services

def deploy_first_phase(origin_bwd, duration):

	fileInfra = "benchmarker_Infra.json"
	infra.deploy_infrastructure(fileInfra, 1, 1)
	services.deploy_services(fileInfra, origin_bwd, duration, 1)

	file = "/home/expran/results/client{}_{}.txt".format(1, origin_bwd)
	fileHandle = open (file, "r")
	lineList = fileHandle.readlines()
	fileHandle.close()
	your_text = lineList[-2].replace(" ", "")

	if(your_text.find('ServerReport:') != -1):
		your_text = lineList[-1].replace(" ", "")

	if(your_text.find("Gbits") > -1):

		bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Gbits")]
		bandwidth = float(bandwidth) * 1000

	elif(your_text.find("Kbits") > -1):
		bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Kbits")]
		bandwidth = float(bandwidth) / 1000

	elif(your_text.find("Mbits") > -1):
		bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Mbits")]
		bandwidth = float(bandwidth)

	origin_bwd = float(origin_bwd)
	dropped = your_text[your_text.find("(")+1:your_text.find("%)")]
	dropped = float(dropped)

	dropped = (((origin_bwd - bandwidth) + (bandwidth * (dropped/100.0)))/origin_bwd)*100

	return dropped

def deploy_second_phase_server(origin_bwd, duration, pktloss):

	for vcpu_count in range (10):

		vcpu = (vcpu_count + 1.0) / 10.0

		print "\033[1m" + "Testing server with", vcpu, "vCPU for", origin_bwd, "Mbps" + "\033[0m"

		fileInfra = "benchmarker_Infra.json"
		infra.deploy_infrastructure(fileInfra, vcpu, 1)
		services.deploy_services(fileInfra, origin_bwd, duration, 2)

		file = "/home/expran/results/client{}_{}_server.txt".format(2, origin_bwd)
		fileHandle = open (file, "r")
		lineList = fileHandle.readlines()
		fileHandle.close()
		your_text = lineList[-2].replace(" ", "")

		if(your_text.find('ServerReport:') != -1):
			your_text = lineList[-1].replace(" ", "")

		if(your_text.find("Gbits") > -1):

			bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Gbits")]
			bandwidth = float(bandwidth) * 1000

		elif(your_text.find("Kbits") > -1):
			bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Kbits")]
			bandwidth = float(bandwidth) / 1000

		elif(your_text.find("Mbits") > -1):
			bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Mbits")]
			bandwidth = float(bandwidth)

		origin_bwd = float(origin_bwd)
		dropped = your_text[your_text.find("(")+1:your_text.find("%)")]
		dropped = float(dropped)

		dropped = (((origin_bwd - bandwidth) + (bandwidth * (dropped/100.0)))/origin_bwd)*100

		print "\033[1m" + "The percentage of packet loss for", vcpu, "vCPU was", dropped, "%" + "\033[0m"
		os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

		if(dropped <= pktloss):
			print "\033[1m" + "So,", vcpu, "vCPU is enough for the server" + "\033[0m"
			break

	return vcpu

def deploy_second_phase_client(origin_bwd, duration, pktloss):

	for vcpu_count in range (10):

		vcpu = (vcpu_count + 1.0) / 10.0

		print "\033[1m" + "Testing client with", vcpu, "vCPU for", origin_bwd, "Mbps" + "\033[0m"

		fileInfra = "benchmarker_Infra.json"
		infra.deploy_infrastructure(fileInfra, 1, vcpu)
		services.deploy_services(fileInfra, origin_bwd, duration, 3)

		file = "/home/expran/results/client{}_{}_client.txt".format(3, origin_bwd)
		fileHandle = open (file, "r")
		lineList = fileHandle.readlines()
		fileHandle.close()
		your_text = lineList[-2].replace(" ", "")

		if(your_text.find('ServerReport:') != -1):
			your_text = lineList[-1].replace(" ", "")

		if(your_text.find("Gbits") > -1):

			bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Gbits")]
			bandwidth = float(bandwidth) * 1000

		elif(your_text.find("Kbits") > -1):
			bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Kbits")]
			bandwidth = float(bandwidth) / 1000

		elif(your_text.find("Mbits") > -1):
			bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Mbits")]
			bandwidth = float(bandwidth)

		origin_bwd = float(origin_bwd)
		dropped = your_text[your_text.find("(")+1:your_text.find("%)")]
		dropped = float(dropped)

		dropped = (((origin_bwd - bandwidth) + (bandwidth * (dropped/100.0)))/origin_bwd)*100

		print "\033[1m" + "The percentage of packet loss for", vcpu, "vCPU was", dropped, "%" + "\033[0m"
		os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

		if(dropped <= pktloss):
			print "\033[1m" + "So,", vcpu, "vCPU is enough for the client" + "\033[0m"
			break

	return vcpu

def deploy_second_phase_server_client (origin_bwd, duration, pktloss, vcpu_server, vcpu_client):

	fileInfra = "benchmarker_Infra.json"
	print "\033[1m" + "Testing with", vcpu_server, "vCPU for the server and", vcpu_client, "vCPU for the client. Throughput is", origin_bwd, "Mbps" + "\033[0m"
	infra.deploy_infrastructure(fileInfra, vcpu_server, vcpu_client)
	services.deploy_services(fileInfra, origin_bwd, duration, 4)

	file = "/home/expran/results/client{}.txt".format(4)
	fileHandle = open (file, "r")
	lineList = fileHandle.readlines()
	fileHandle.close()
	your_text = lineList[-2].replace(" ", "")

	if(your_text.find('ServerReport:') != -1):
		your_text = lineList[-1].replace(" ", "")

	if(your_text.find("Gbits") > -1):

		bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Gbits")]
		bandwidth = float(bandwidth) * 1000

	elif(your_text.find("Kbits") > -1):
		bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Kbits")]
		bandwidth = float(bandwidth) / 1000

	elif(your_text.find("Mbits") > -1):
		bandwidth = your_text[your_text.find("Bytes")+5:your_text.find("Mbits")]
		bandwidth = float(bandwidth)

	origin_bwd = float(origin_bwd)
	dropped = your_text[your_text.find("(")+1:your_text.find("%)")]
	dropped = float(dropped)

	dropped = (((origin_bwd - bandwidth) + (bandwidth * (dropped/100.0)))/origin_bwd)*100
	os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

	print "The percentage of packet loss with", vcpu_server, "vCPU for the server and", vcpu_client, "vCPU for the client was", dropped, "%"
	print "\033[1m" + "The recommendation of the benchmarker is: To achieve", pktloss, "%" + " of packet loss, you should use", vcpu_server, "vCPU for the server and", vcpu_client, "vCPU for the client. Throughput should be", origin_bwd, "Mbps." + "\033[0m"
	print "Benchmarker finished!"

def main ():

	parser = argparse.ArgumentParser()
	
	parser.add_argument("-b", "--bwd", help="Bandwidth")
	parser.add_argument("-p", "--pktloss", help="Packet loss goal")
	parser.add_argument("-d", "--duration", help="Duration of each test")
	parser.add_argument("-s1", "--series1", help="First number of the series")
	parser.add_argument("-s2", "--series2", help="Second number of the series")

	args = parser.parse_args()

	dropped = 100.0
	i = 1
	bandwidth = float(args.bwd)
	accepted_drop = float(args.pktloss)
	duration = int(args.duration)

	if(args.series1 and args.series2):

		series1 = float(args.series1)
		series2 = float(args.series2)

		while(dropped > accepted_drop):

			if(i == 1):
				print "\033[1m" + "Running test 1 - throughput is", bandwidth, "Mbps" + "\033[0m"
				dropped = deploy_first_phase(bandwidth, duration)
				print "\033[1m" + "The percentage of packet loss was", dropped, "%" + "\033[0m"
				os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

			elif(i % 2 == 0):
				print ("Scaling the bandwidth by diving by {}".format(series1))
				bandwidth = bandwidth / series1
				print "\033[1m" + "Running test", i, "- throughput is", bandwidth, "Mbps" + "\033[0m"
				dropped = deploy_first_phase(bandwidth, duration)
				print "\033[1m" + "The percentage of packet loss was", dropped, "%" + "\033[0m"
				os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

			elif(i % 2 != 0 and i != 1):
				print ("Scaling the bandwidth by diving by {}".format(series2))
				bandwidth = bandwidth / series2
				print "\033[1m" + "Running test", i, "- throughput is", bandwidth, "Mbps" + "\033[0m"
				dropped = deploy_first_phase(bandwidth, duration)
				print "\033[1m" + "The percentage of packet loss was", dropped, "%" + "\033[0m"
				os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

			i += 1
	else:

		while(dropped > accepted_drop):

			if(i == 1):
				print "\033[1m" + "Running test 1 - throughput is", bandwidth, "Mbps" + "\033[0m"
				dropped = deploy_first_phase(bandwidth, duration)
				print "\033[1m" + "The percentage of packet loss was", dropped, "%" + "\033[0m"
				os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

			elif(i % 2 == 0):
				print ("Scaling the bandwidth by diving by 2")
				bandwidth = bandwidth / 2.0
				print "\033[1m" + "Running test", i, "- throughput is", bandwidth, "Mbps" + "\033[0m"
				dropped = deploy_first_phase(bandwidth, duration)
				print "\033[1m" + "The percentage of packet loss was", dropped, "%" + "\033[0m"
				os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

			elif(i % 2 != 0 and i != 1):
				print ("Scaling the bandwidth by diving by 10")
				bandwidth = bandwidth / 10.0
				print "\033[1m" + "Running test", i, "- throughput is", bandwidth, "Mbps" + "\033[0m"
				dropped = deploy_first_phase(bandwidth, duration)
				print "\033[1m" + "The percentage of packet loss was", dropped, "%" + "\033[0m"
				os.system("python destroy_emulation.py -u n -i benchmarker_Infra.json")

			i += 1

	print "\033[1m" + "First phase of the benchmarker finished. The recommended bandwidth for", accepted_drop, "% packet loss is", bandwidth, "Mbps" + "\033[0m"

	print ("Now let's go to the second phase of the benchmarker")
	print ("We are going to test what percentage of vCPU is enough to generate and to process the network traffic")
	print ("Let's start with the server side")

	vcpu_server = deploy_second_phase_server(bandwidth, duration, accepted_drop)

	print ("Now let's test the client")

	vcpu_client = deploy_second_phase_client(bandwidth, duration, accepted_drop)

	print ("Now let's test the recommended vCPU for the server {} vCPU with the recommended vCPU for the client {} vCPU".format(vcpu_server, vcpu_client))

	deploy_second_phase_server_client(bandwidth, duration, accepted_drop, vcpu_server, vcpu_client)

if __name__ == '__main__':
    main()
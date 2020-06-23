# -*- coding: utf-8 -*-

import argparse

import infrastructure_manager as infra
import network_rules as net_rules
import service_manager as services

def main ():

	parser = argparse.ArgumentParser()
	
	parser.add_argument("-e", "--emultype", help="Emulation type")
	parser.add_argument("-t", "--time", help="Duration of the test")
	parser.add_argument("-i", "--infra", help="Infrastructure file")
	parser.add_argument("-s", "--service", help="Service file")
	parser.add_argument("-b", "--default_bwd", help="Default bandwidth limitation in the interface")

	args = parser.parse_args()

	if(args.default_bwd):
		infra.deploy_infrastructure(args.emultype, args.infra)
		net_rules.deploy_net_rules(args.emultype, args.infra, args.service)
		services.deploy_services(args.emultype, args.time, args.infra, args.service, args.default_bwd)

	else:
		args.default_bwd = float(0.0)
		infra.deploy_infrastructure(args.emultype, args.infra)
		net_rules.deploy_net_rules(args.emultype, args.infra, args.service)
		services.deploy_services(args.emultype, args.time, args.infra, args.service, args.default_bwd)

if __name__ == '__main__':
	main()
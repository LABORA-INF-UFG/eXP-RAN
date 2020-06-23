# -*- coding: utf-8 -*-

import argparse
import infrastructure_destroy as destroy

def main ():

	parser = argparse.ArgumentParser()
	
	parser.add_argument("-u", "--userdel", help="Delete eXP-RAN user")
	parser.add_argument("-i", "--infra", help="Infrastructure file")

	args = parser.parse_args()

	destroy.destroy_infra(args.userdel, args.infra)

if __name__ == '__main__':
	main()
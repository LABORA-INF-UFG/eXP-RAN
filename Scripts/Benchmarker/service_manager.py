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

def deploy_services(fileInfra, origin_bwd, duration, phase):

	bandwidth = origin_bwd
	flow_server = 1 #recp
	flow_client = 2 #gen
	VMserverip = '169.254.1.1' #recp
	VMclientip = '169.254.2.2' #gen

	if(phase == 1):

		# Subindo server
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn1 sh -c "iperf -s -u -e -i 1 > server{}_{}.txt"'.format(phase, bandwidth))
		ssh.close()

		# Subindo client
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn2 sh -c "iperf -c 192.168.1.1 -u -b {}m -e -i 1 -t {} > client{}_{}.txt"'.format(bandwidth, duration, phase, bandwidth))
		ssh.close()

		time.sleep(int(duration) + 5)

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn1:/server{}_{}.txt /root/server{}_{}.txt'.format(phase, bandwidth, phase, bandwidth))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn2:/client{}_{}.txt /root/client{}_{}.txt'.format(phase, bandwidth, phase, bandwidth))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		time.sleep(5)

	elif(phase == 2):

		# Subindo server
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn1 sh -c "iperf -s -u -e -i 1 > server{}_{}_server.txt"'.format(phase, bandwidth))
		ssh.close()

		# Subindo client
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn2 sh -c "iperf -c 192.168.1.1 -u -b {}m -e -i 1 -t {} > client{}_{}_server.txt"'.format(bandwidth, duration, phase, bandwidth))
		ssh.close()

		time.sleep(int(duration) + 5)

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn1:/server{}_{}_server.txt /root/server{}_{}_server.txt'.format(phase, bandwidth, phase, bandwidth))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn2:/client{}_{}_server.txt /root/client{}_{}_server.txt'.format(phase, bandwidth, phase, bandwidth))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		time.sleep(5)

	elif(phase == 3):

		# Subindo server
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn1 sh -c "iperf -s -u -e -i 1 > server{}_{}_client.txt"'.format(phase, bandwidth))
		ssh.close()

		# Subindo client
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn2 sh -c "iperf -c 192.168.1.1 -u -b {}m -e -i 1 -t {} > client{}_{}_client.txt"'.format(bandwidth, duration, phase, bandwidth))
		ssh.close()

		time.sleep(int(duration) + 5)

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn1:/server{}_{}_client.txt /root/server{}_{}_client.txt'.format(phase, bandwidth, phase, bandwidth))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn2:/client{}_{}_client.txt /root/client{}_{}_client.txt'.format(phase, bandwidth, phase, bandwidth))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		time.sleep(5)

	elif(phase == 4):

		# Subindo server
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn1 sh -c "iperf -s -u -e -i 1 > server{}.txt"'.format(phase))
		ssh.close()

		# Subindo client
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker exec -d ctn2 sh -c "iperf -c 192.168.1.1 -u -b {}m -e -i 1 -t {} > client{}.txt"'.format(bandwidth, duration, phase))
		ssh.close()

		time.sleep(int(duration) + 5)

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMserverip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn1:/server{}.txt /root/server{}.txt'.format(phase, phase))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(VMclientip, username='root', password='necos')
		stdin, stdout, stderr = ssh.exec_command('docker cp ctn2:/client{}.txt /root/client{}.txt'.format(phase, phase))
		time.sleep(5)
		stdin, stdout, stderr = ssh.exec_command('python file_copier.py /home/expran/results')
		ssh.close()

		time.sleep(5)
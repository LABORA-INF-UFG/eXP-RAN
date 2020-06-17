# eXP-RAN - an Emulator for Gaining Experience with Radio Access Networks, Edge Computing, and Slicing

eXP-RAN was tested on Ubuntu 18.04 LTS and Ubuntu Server 18.04 LTS. Although it may work in some other Debian-based Linux distributions, we do not guarantee that all features will work well.

- [Getting started](#getting-started)
- [Running your tests](#running-your-tests)
	- [Topology Generator](#topology-generator)

## Getting started

These instructions will guide you to get eXP-RAN up and running.

### Installing the prerequisites

```
sudo apt update
sudo apt install python net-tools unzip python-pip iproute2 xen-hypervisor-4.6-amd64 xen-tools openvswitch-switch openssh-server curl git
sudo pip install paramiko networkx
```

### Xen configuration

After installing the Xen Hypervisor, you need to restart your computer to load the hypervisor.

Optional extra configuration: It is highly recommend to configure the Xen dom0 RAM, more information regarding this configuration can be found on the Xen Project Documentation:

* [Xen Project Best Practices](https://wiki.xenproject.org/wiki/Xen_Project_Best_Practices) - Xen dom0 RAM configuration

### Cloning the repository

```
git clone https://github.com/LABORA-INF-UFG/eXP-RAN
```

### Downloading the VM Template

Now you need to download eXP-RAN's Xen VM.

In order to do that, first enter the Xen VM subdirectory inside the repository you just cloned.

Make sure that the location of the Xen VM directory is correct, the directory may differ depending on in which directory you have cloned the project.

```
cd /home/$USER/eXP-RAN/XenVM/
```

Then, run the VM Downloader script.

```
sh VMDownloader.sh
```

Once that is done, you should have two files downloaded to your machine, one is the VM disk and the other is the VM swap disk.

### Creating the eXP-RAN user

In order for eXP-RAN to save the results of the tests from the VMs to your host, you need to create a user on your host for eXP-RAN.

This is necessary because eXP-RAN copy the results from the VMs to your host via SCP, and instead of asking for the user's password to transfer the files, a more secure approach is to a create a user without root permissions only to copy the results files.

* [SSH/TransferFiles - Secure Copy (SCP)](https://help.ubuntu.com/community/SSH/TransferFiles)

To create your non-root eXP-RAN user, simply type:

```
sudo useradd -m expran -s /bin/bash
```

For eXP-RAN to work properly, the eXP-RAN user password has to be "necos". You must change eXP-RAN's password with the following command:

```
sudo passwd expran
```

Then, type necos for "Enter new UNIX password:" and "Retype new UNIX password:".

Remember that this user is a non-root user and it is only going to be used for SCP, so the are no big security issues regarding the creation of this user.

Nonetheless, you can delete this user at any moment by typing:

```
sudo userdel expran && sudo rm -rf /home/expran
```

Alternatively, eXP-RAN has a module to destroy the created infrastructure. This module already deletes eXP-RAN's user after the emulation is done.

Now eXP-RAN is fully configured and you can start your tests!

## Running your tests

There are three ways in which the user can interact with the tool. The figure below details how the interactions.

<div align="center">
<img src="Figures/System_Components.jpg" >
</div>

The figure above represents eXP-RAN workflow and system modules.

Dot arrows represent optional flow; double arrows identify user inputs; single arrows represent mandatory flow; rectangle with dashed lines represent input files; while rectangle with solid lines identify the system modules.

Let's start with the Topology Generator module.

### Topology Generator

The topology generator is designed to generate random RAN topologies.

We use a Waxman graph to generate the topology, a type of graph very similar to the topologies usually found in RANs.

* [More information about the Waxman graph](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.generators.geometric.waxman_graph.html)

The topology generator is at Scripts/Topology_Generator

You can run the topology generator by running the following script combined with the Waxman arguments:

```
python top_gen.py -u USERNAME -n NumberOfNodes -a Alpha -b Beta -l L
```

Where:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -u (string) – Your username.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -n (int) – Number of nodes.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -a (float) – Alpha Model parameter.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -b (float) – Beta Model parameter.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -l (float) – Maximum distance between nodes.

The default arguments are:

```
python top_gen.py -u John -n 3 -a 0.4 -b 0.1 -l 70
```

The JSON output containing the topology description is located at the same directory of the topology generator script.

Keep in mind that only the RAN topology is generated. The user needs to create the Docker containers information as well as the service file.

However, the topology generator helps users with limited knowledge of RAN/EC scenarios and supports educational purposes.
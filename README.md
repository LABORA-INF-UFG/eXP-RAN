# eXP-RAN - an Emulator for Gaining Experience with Radio Access Networks, Edge Computing, and Slicing

eXP-RAN was tested on Ubuntu 18.04 LTS and Ubuntu Server 18.04 LTS. Although it may work in some other Debian-based Linux distributions, we do not guarantee that all features will work well.

- [Getting started](#getting-started)
- [Running your tests](#running-your-tests)

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

Now eXP-RAN is fully configured and you can start your tests!

## Running your tests
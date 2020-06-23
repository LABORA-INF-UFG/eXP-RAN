class Node():
  def __init__(self, id, type):
    self.id = id
    self.type = type
    self.vms = []

class Link():
  def __init__(self):
    # TODO
    pass

class VM():
  def __init__(self, id, cpu, ram):
    self.id = id
    self.cpu = cpu
    self.ram = ram
    self.containers = []

  def add_container(self, ctn):
    self.containers.append(ctn)
    self.cpu += ctn.cpu
    self.ram += ctn.ram

class Container():
  def __init__(self, id, cpu, ram):
    self.id = id
    self.cpu = cpu
    self.ram = ram

class Network():
  def __init__(self):
    self.nodes = []
    self.links = []
    self.switches = {}
    self.switch_at_node = {}

  def add_node(self, node):
    self.nodes.append(node)
  
  def add_link(self, link):
    self.links.append(link)

  def set_switch(self, s_name, switch):
    self.switches[s_name] = switch
    self.switches[switch.bound_node] = switch

  def get_switch(self, s_name, bound_node):
    if s_name not in self.switches:
      sw = Switch(s_name, bound_node)
      self.switches[s_name] = sw
      self.switch_at_node[bound_node] = sw

    return self.switches[s_name]

class Switch():
  def __init__(self, name, bound_node):
    self.name = name
    self.interfaces = []
    self.interfaces_by_patch = {}
    self.reachable = set()
    self.bound_node = bound_node

  def add_interface(self, interface):
    self.interfaces.append(interface)
    self.interfaces_by_patch[interface.patch] = interface
    self.reachable.add(interface.patch)

  def get_interface(self, reachable):
    return self.interfaces_by_patch[reachable]

class Interface():
  def __init__(self, name, patch):
    self.name = name
    self.patch = patch

class Flow_vran():
  def __init__(self, source_node, target_node, source_ip, target_ip, path, bw, tos):
    self.source_node = source_node
    self.target_node = target_node
    self.source_ip = source_ip
    self.target_ip = target_ip
    self.path = path
    self.bw = bw
    self.tos = tos

class Flow_video():
  def __init__(self, source_node, target_node, source_ip, target_ip, path):
    self.source_node = source_node
    self.target_node = target_node
    self.source_ip = source_ip
    self.target_ip = target_ip
    self.path = path

network = Network()
import os

class NetController():

  @staticmethod
  def apply_rules_vran(flow, network, apply_arp):

    for i in range(0, len(flow.path)):

      target_ip = flow.target_ip
      tos = flow.tos
      resident = flow.path[i]
      switch = network.switch_at_node[resident]

      if i == 0:

        source = resident
        target = flow.path[i + 1]
        in_iface = switch.interfaces_by_patch[source]
        out_iface = switch.interfaces_by_patch[target]
        os.system("ovs-ofctl add-flow {} in_port={},udp,nw_dst={},nw_tos={},actions={}".format(switch.name, in_iface.name, target_ip, tos, out_iface.name))

        if apply_arp:
          os.system("ovs-ofctl add-flow {} arp,nw_src={},actions={}".format(switch.name, flow.source_ip, out_iface.name))
          os.system("ovs-ofctl add-flow {} arp,nw_dst={},actions={}".format(switch.name, flow.source_ip, in_iface.name))

      elif i == (len(flow.path) - 1):

        source = flow.path[i - 1]
        target = resident
        in_iface = switch.interfaces_by_patch[source]
        out_iface = switch.interfaces_by_patch[target]
        os.system("ovs-ofctl add-flow {} in_port={},udp,nw_dst={},nw_tos={},actions={}".format(switch.name, in_iface.name, target_ip, tos, out_iface.name))

        if apply_arp:
          os.system("ovs-ofctl add-flow {} arp,nw_src={},actions={}".format(switch.name, flow.source_ip, out_iface.name))
          os.system("ovs-ofctl add-flow {} arp,nw_dst={},actions={}".format(switch.name, flow.source_ip, in_iface.name))

      else:

        source = flow.path[i - 1]
        target = flow.path[i + 1]
        in_iface = switch.interfaces_by_patch[source]
        out_iface = switch.interfaces_by_patch[target]
        os.system("ovs-ofctl add-flow {} in_port={},udp,nw_dst={},nw_tos={},actions={}".format(switch.name, in_iface.name, target_ip, tos, out_iface.name))

        if apply_arp:
          os.system("ovs-ofctl add-flow {} arp,nw_src={},actions={}".format(switch.name, flow.source_ip, out_iface.name))
          os.system("ovs-ofctl add-flow {} arp,nw_dst={},actions={}".format(switch.name, flow.source_ip, in_iface.name))

  @staticmethod
  def apply_rules_video(flow, network):

    for i in range(0, len(flow.path)):

      target_ip = flow.target_ip
      resident = flow.path[i]
      switch = network.switch_at_node[resident]

      if i == 0:
        
        source = resident
        target = flow.path[i + 1]
        in_iface = switch.interfaces_by_patch[source]
        out_iface = switch.interfaces_by_patch[target]

        os.system("ovs-ofctl add-flow {} in_port={},udp,nw_dst={},actions={}".format(switch.name, in_iface.name, target_ip, out_iface.name))
        os.system("ovs-ofctl add-flow {} arp,nw_src={},actions={}".format(switch.name, flow.source_ip, out_iface.name))
        os.system("ovs-ofctl add-flow {} arp,nw_dst={},actions={}".format(switch.name, flow.source_ip, in_iface.name))

      elif i == (len(flow.path) - 1):

        source = flow.path[i - 1]
        target = resident
        in_iface = switch.interfaces_by_patch[source]
        out_iface = switch.interfaces_by_patch[target]

        os.system("ovs-ofctl add-flow {} in_port={},udp,nw_dst={},actions={}".format(switch.name, in_iface.name, target_ip, out_iface.name))
        os.system("ovs-ofctl add-flow {} arp,nw_src={},actions={}".format(switch.name, flow.source_ip, out_iface.name))
        os.system("ovs-ofctl add-flow {} arp,nw_dst={},actions={}".format(switch.name, flow.source_ip, in_iface.name))

      else:

        source = flow.path[i - 1]
        target = flow.path[i + 1]
        in_iface = switch.interfaces_by_patch[source]
        out_iface = switch.interfaces_by_patch[target]

        os.system("ovs-ofctl add-flow {} in_port={},udp,nw_dst={},actions={}".format(switch.name, in_iface.name, target_ip, out_iface.name))
        os.system("ovs-ofctl add-flow {} arp,nw_src={},actions={}".format(switch.name, flow.source_ip, out_iface.name))
        os.system("ovs-ofctl add-flow {} arp,nw_dst={},actions={}".format(switch.name, flow.source_ip, in_iface.name))
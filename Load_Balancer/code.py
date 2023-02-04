from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr
import time
conn = True
ctr = 0  
log = core.getLogger()

class MyHub (object):


    def __init__ (self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

    def _handle_PacketIn (self, event):
        # Handles packet in messages from the switch.
        global conn
        global ctr
        ctr = ctr + 1
        if(ctr%3 == 0): 
            conn = not conn
            ctr = 1
        print("Hello ", conn)
        log.debug("Got PktIn.\n")
        # print("Buffer ID: %s\n" % event.ofp.buffer_id)
        log.debug("Whole PktIn: %s" % (event.ofp))

        if conn:
            msg = of.ofp_flow_mod()
            msg.priority = 200
            msg.idle_timeout = 10
            msg.match.in_port = event.ofp.in_port
            msg.match.dl_type = 0x800
            msg.match.nw_dst = IPAddr("10.0.0.3")
            msg.match.nw_proto = 6
            msg.match.tp_dst = 80

            msg.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("00:00:00:00:00:04")))
            msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("10.0.0.4")))
            msg.actions.append(of.ofp_action_output(port = 4))
            # Send message to switch
            self.connection.send(msg)
		
		
        if not conn:
        	
            msg = of.ofp_flow_mod()
            msg.priority = 200
            msg.idle_timeout = 10
            msg.match.in_port = event.ofp.in_port
            msg.match.dl_type = 0x800
            msg.match.nw_dst = IPAddr("10.0.0.3")
            msg.match.nw_proto = 6
            msg.match.tp_dst = 80

            msg.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("00:00:00:00:00:05")))
            msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("10.0.0.5")))
            msg.actions.append(of.ofp_action_output(port = 5))
            # Send message to switch
            self.connection.send(msg)
		
        

	
        msg = of.ofp_packet_out()
        msg.data = event.ofp.data
        msg.in_port = event.ofp.in_port 
        # Add an action to send to the specified port
        action = of.ofp_action_output(port = of.OFPP_TABLE)
        msg.actions.append(action)

        # Send message to switch
        self.connection.send(msg)



def launch ():
    
    def start_switch (event):

        log.debug("Controlling %s" % (event.connection,))
        MyHub(event.connection)

        msg = of.ofp_flow_mod()
        #ovs-ofctl add-flow s1 priority=100,in_port=1,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.3,tp_dst=80,actions=controller
        msg.priority = 100
        msg.match.in_port = 1
        msg.match.dl_type = 0x800
        msg.match.nw_dst = IPAddr("10.0.0.3")
        msg.match.nw_proto = 6
        msg.match.tp_dst = 80
        msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
        event.connection.send(msg)
        
        #ovs-ofctl add-flow s1 priority=100,in_port=2,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.3,tp_dst=80,actions=controller
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.match.in_port = 2
        msg.match.dl_type = 0x800
        msg.match.nw_dst = IPAddr("10.0.0.3")
        msg.match.nw_proto = 6
        msg.match.tp_dst = 80
        msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
        event.connection.send(msg)
        
        #ovs-ofctl add-flow s1 priority=98,in_port=4,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.1,tp_src=80,actions=mod_dl_src:00:00:00:00:00:03,mod_nw_src:10.0.0.3,output:1
        msg = of.ofp_flow_mod()
        msg.priority = 98
        msg.match.in_port = 4
        msg.match.dl_type = 0x800
        msg.match.nw_dst = IPAddr("10.0.0.1")
        msg.match.nw_proto = 6
        msg.match.tp_src = 80
        msg.actions.append(of.ofp_action_dl_addr.set_src(EthAddr("00:00:00:00:00:03")))
        msg.actions.append(of.ofp_action_nw_addr.set_src(IPAddr("10.0.0.3")))
        msg.actions.append(of.ofp_action_output(port = 1))
        event.connection.send(msg)
        
        
        
        #ovs-ofctl add-flow s1 priority=98,in_port=5,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.1,tp_src=80,actions=mod_dl_src:00:00:00:00:00:03,mod_nw_src:10.0.0.3,output:1
        msg = of.ofp_flow_mod()
        msg.priority = 98
        msg.match.in_port = 5
        msg.match.dl_type = 0x800
        msg.match.nw_dst = IPAddr("10.0.0.1")
        msg.match.nw_proto = 6
        msg.match.tp_src = 80
        msg.actions.append(of.ofp_action_dl_addr.set_src(EthAddr("00:00:00:00:00:03")))
        msg.actions.append(of.ofp_action_nw_addr.set_src(IPAddr("10.0.0.3")))
        msg.actions.append(of.ofp_action_output(port = 1))
        event.connection.send(msg)
        
        
        #ovs-ofctl add-flow s1 priority=98,in_port=4,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.2,tp_src=80,actions=mod_dl_src:00:00:00:00:00:03,mod_nw_src:10.0.0.3,output:2
        msg = of.ofp_flow_mod()
        msg.priority = 98
        msg.match.in_port = 4
        msg.match.dl_type = 0x800
        msg.match.nw_dst = IPAddr("10.0.0.2")
        msg.match.nw_proto = 6
        msg.match.tp_src = 80
        msg.actions.append(of.ofp_action_dl_addr.set_src(EthAddr("00:00:00:00:00:03")))
        msg.actions.append(of.ofp_action_nw_addr.set_src(IPAddr("10.0.0.3")))
        msg.actions.append(of.ofp_action_output(port = 2))
        event.connection.send(msg)
        
        
        #ovs-ofctl add-flow s1 priority=98,in_port=5,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.2,tp_src=80,actions=mod_dl_src:00:00:00:00:00:03,mod_nw_src:10.0.0.3,output:2
        msg = of.ofp_flow_mod()
        msg.priority = 98
        msg.match.in_port = 5
        msg.match.dl_type = 0x800
        msg.match.nw_dst = IPAddr("10.0.0.2")
        msg.match.nw_proto = 6
        msg.match.tp_src = 80
        msg.actions.append(of.ofp_action_dl_addr.set_src(EthAddr("00:00:00:00:00:03")))
        msg.actions.append(of.ofp_action_nw_addr.set_src(IPAddr("10.0.0.3")))
        msg.actions.append(of.ofp_action_output(port = 2))
        event.connection.send(msg)
        
        
        #ovs-ofctl add-flow s1 priority=90,actions=drop
        msg = of.ofp_flow_mod()
        msg.priority = 90
        event.connection.send(msg)
        
    core.openflow.addListenerByName("ConnectionUp", start_switch)

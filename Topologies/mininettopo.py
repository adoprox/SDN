#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    #s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    #s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    #s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    #s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, protocols='OpenFlow13')
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', mac='00:00:00:00:00:01', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', mac='00:00:00:00:00:02', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', mac='00:00:00:00:00:03', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', mac='00:00:00:00:00:04', defaultRoute=None)

    info( '*** Add links\n')
    h1s1 = {'bw':200}
    net.addLink(h1, s1, cls=TCLink , **h1s1)
    s1h2 = {'bw':100}
    net.addLink(s1, h2, cls=TCLink , **s1h2)
    s3h3 = {'bw':100}
    net.addLink(s3, h3, cls=TCLink , **s3h3)
    s4h4 = {'bw':100}
    net.addLink(s4, h4, cls=TCLink , **s4h4)
    s1s2 = {'bw':100}
    net.addLink(s1, s2, cls=TCLink , **s1s2)
    s1s3 = {'bw':100}
    net.addLink(s1, s3, cls=TCLink , **s1s3)
    s2s4 = {'bw':100}
    net.addLink(s2, s4, cls=TCLink , **s2s4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])

    info( '*** Post configure switches and hosts\n')
    
    # Esegui il ping tra h1 e h2 per 4 volte e viceversa
    for _ in range(4):
        net.get('h1').cmd('ping -c 1 10.0.0.2')
        net.get('h2').cmd('ping -c 1 10.0.0.1')

    # Esegui il ping tra h3 e h4 per 4 volte e viceversa
    for _ in range(4):
        net.get('h3').cmd('ping -c 1 10.0.0.4')
        net.get('h4').cmd('ping -c 1 10.0.0.3')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


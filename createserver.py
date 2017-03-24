#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Joerg.schulz@ts.fujitsu.com

calls K5 routines of Graham Land
Date: 16/03/17

Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


creates a Server - if it exists already, we return info on that server.


"""

import config
import fjk5

if config.testing :
    import pdb
import listServers


def main():
    print (usage)
    # here we get the login token as key for all other info
    token = fjk5.get_scoped_token()
    
    # before we start we need info about the network
    networks, status = fjk5.list_networks(token)
    securityGroup = fjk5.getSecurityGroup(token, config.securityGroup )
    
    if status < 400 :
        network = filter(lambda name: name['name'] == config.networkName, networks.json()['networks'])
        networkID = network[0]['id']
        print ('network %s: ' % networkID)
        # create a port
        portInfo = fjk5.create_port(token, networkID, security_group_id = securityGroup['id'] if securityGroup else False)
        
        port = portInfo.json()['port'].get('id')
        # this one creates the server
        
        serverInfo = fjk5.create_server(token, port = port)
        print (serverInfo)
        # if config.testing: pdb.set_trace()
        print (serverInfo.content)
    else :
        print ("error %s: " % response.status_code)
    # something weird with security groups, so list them
    

    # next we add a public IP to that port
    extNetwork = filter(lambda name: name['name'] == config.externalNet, networks.json()['networks'])
    # obviously we have to wait a while before assigning a publich ip
    publicNetwork = fjk5.create_global_ip(token, extNetwork[0]['id'], port)
    print (publicNetwork.json()['floatingip']['floating_ip_address'])
    # dispay the most important infos here: IP, vnc
    listServers.listServers
    pdb.set_trace()
    initPassword = fjk5.get_Serverpassword(token, serverInfo.json()['server']['id'])
    pdb.set_trace()
    

    
    
    

    


if __name__ == "__main__":
    main()
#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Joerg.schulz@ts.fujitsu.com

calls K5 routines of Graham Land
Date: 16/03/17

Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


creates a Network - if it exists already, we return info on that network.

"""

import config
import fjk5

if config.testing :
    import pdb



def main():
    print (usage)
    # here we get the login token as key for all other info
    token = fjk5.get_scoped_token()
    theToken = token.headers['X-Subject-Token']
    # print(theToken)
    # before we start we need info about the network
    networks, status = fjk5.list_networks(token)
    if status < 400 : # we now have a list of dictionaries containing the network
        network = filter(lambda name: name['name'] == config.networkName, networks.json()['networks'])
        # if this net doesn't exist, we create it
        if len(network) == 0:
            ourNetwork = fjk5.create_network(token)
            networkID = ourNetwork.json()['network']['id']
            subnet = fjk5.create_subnet(token, networkID)
        else:
            networkID = network[0]['id']
            subnet = network[0]['subnets']
        # networkID = networks.json()['networks'][config.networkIndex].get('id')
        print ('network %s: ' % networkID)
        
    else :
        print ("error %s: " % response.status_code)
    # we need a router
    routers, status = fjk5.list_routers(token)
    
    router = filter(lambda name: name['name'] == config.routerName, routers.json()['routers'])
    if len(router) == 0 :
        ourRouter = fjk5.create_router(token)
        routerID = ourRouter.json()['router']['id']
        # now this router needs some networks
        extNetwork = filter(lambda name: name['name'] == config.externalNet, networks.json()['networks'])
        updatedRouter = fjk5.update_router_gateway(token, routerID, extNetwork[0]['id'])
        routerID = updatedRouter.json()['router']['id']
        router_interface = fjk5.add_interface_to_router(token, ourRouter.json()['router']['id'], subnet.json()['subnet']['id'])
        
    else:
        routerID = router[0]['id']

        
    if config.testing: pdb.set_trace()
    
    
    


    

    


if __name__ == "__main__":
    main()
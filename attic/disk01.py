import os
import sys
import time
from optparse import OptionParser

import googleapiclient.discovery

from instance import wait_for_operation

def create(compute, disk_name, size, project="cidc-biofx", zone="us-east1-b"):
    """Given a XX, YYY...
    Tries to create an disk according to the given params using 
    googeapi methods"""

    disk_config = {'name': "", "sizeGb": "", "zone": ""}

    #set the config
    disk_config['name'] = disk_name
    disk_config['sizeGb'] = size
    disk_config['zone'] = zone
    #print(disk_config)

    #create disk
    operation = compute.disks().insert(
        project=project,
        zone=zone,
        body=disk_config).execute()
    wait_for_operation(compute, project, zone, operation['name'])
    #print(operation)
    return operation

def delete(compute, disk_name, project="cidc-biofx", zone="us-east1-b"):
    #based on From google tutorial!
    operation = compute.disks().delete(
        project=project,
        zone=zone,
        disk=disk_name).execute()
    wait_for_operation(compute, project, zone, operation['name'])
    #print(operation)
    return operation


def attach_disk(compute, instance_name, disk_name, project="cidc-biofx", zone="us-east1-b"):

    #get the disk resource
    operation = compute.disks().get(
        project=project,
        zone=zone,
        disk=disk_name).execute()
    diskLink = operation['selfLink']
    attached_disk_body = {'source':diskLink}

    #attach disk
    operation = compute.instances().attachDisk(
        project=project,
        zone=zone,
        instance=instance_name,
        body=attached_disk_body).execute()
    wait_for_operation(compute, project, zone, operation['name'])
    #print(operation)
    return operation


#TODO:
def detach_disk(compute, instance_name, disk_name, project="cidc-biofx", zone="us-east1-b"):
    print("detach_disk is not implemented!")
    return
    #get the disk resource
    operation = compute.disks().get(
        project=project,
        zone=zone,
        disk=disk_name).execute()
    #print(operation)
    #sys.exit()
    diskLink = operation['selfLink']

    #attached_disk_body = {'source':diskLink}
    attached_disk_body = {"source": "zones/%s/disks/%s" % (zone, disk_name)}

    #attach disk
    operation = compute.instances().detachDisk(
        project=project,
        zone=zone,
        instance=instance_name,
        #body=attached_disk_body).execute()
        deviceName='wes-auto-disk').execute()
    wait_for_operation(compute, project, zone, operation['name'])
    #print(operation)
    return operation
    
def main():
    compute = googleapiclient.discovery.build('compute', 'v1')
    #TODO: update this!

    # operation = compute.disks().get(
    #     project='cidc-biofx',
    #     zone='us-east1-b',
    #     disk='disk-4').execute()
    # print(operation)
    # sys.exit()
    # wait_for_operation(compute, 'cidc-biofx', 'us-east1-b', operation['name'])
    # print(operation)
    # sys.exit()

    #attach_disk(compute, "wes-develop", "wes-auto-disk", project="cidc-biofx", zone='us-east1-b')
    #attach_disk(compute, "wes-develop", "wes-auto-disk", 'us-east1-b')
    detach_disk(compute, "wes-develop", "wes-auto-disk", project="cidc-biofx", zone='us-east1-b')
if __name__=='__main__':
    main()

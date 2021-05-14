#!/usr/bin/env python

import time
import googleapiclient.discovery

#globals
zone="us-east1-b"
project="cidc-biofx"
name=instance_name="wes-auto-1"
disk_size="20" #GB

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)

#REQUIRED auth
compute = googleapiclient.discovery.build('compute', 'v1')

#create new disk
disk_config = {'name': "%s-ssd" % name, "sizeGb": disk_size, "zone": zone}
operation = compute.disks().insert(
    project=project,
    zone=zone,
    body=disk_config).execute()
#print(operation)
wait_for_operation(compute, project, zone, operation['name'])
#get the disk url
diskLink = operation['targetLink']

#This gets the latest image
image_response = compute.images().getFromFamily(
    project=project, family='wes').execute()
#print(image_response)
source_disk_image = image_response['selfLink']

#set the machine type
machine_type = "zones/%s/machineTypes/n1-standard-1" % zone



#configure the instance


config = {
    'name': name,
    'machineType': machine_type,
    
    # Specify the boot disk and the image to use as a source.
    'disks': [
        {
            'boot': True,
            'autoDelete': True,
            'initializeParams': {
                'sourceImage': source_disk_image,
            }
        },
        {
            #"deviceName": "%s_ssd" % name,
            'source': diskLink,
        },

    ],
    
    # Specify a network interface with NAT to access the public
    # internet.
    'networkInterfaces': [{
        'network': 'global/networks/default',
        'accessConfigs': [
            {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
        ]
    }],

    # Allow the instance to access cloud storage and logging.
    'serviceAccounts': [{
        'email': 'biofxvm@cidc-biofx.iam.gserviceaccount.com',
        #'email': 'default',
        'scopes': [
            'https://www.googleapis.com/auth/devstorage.read_write',
            'https://www.googleapis.com/auth/logging.write'
        ]
    }],

    # Metadata is readable from the instance and allows you to
    # pass configuration from deployment scripts to instances.
    'metadata': {
    }
}

operation = compute.instances().insert(
    project=project,
    zone=zone,
    body=config).execute()
wait_for_operation(compute, project, zone, operation['name'])

#instances = list_instances(compute, project, zone)
#print('Instances in project %s and zone %s:' % (project, zone))
#for instance in instances:
#    print(' - ' + instance['name'])


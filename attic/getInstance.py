import os
import sys
import time
from optparse import OptionParser

import googleapiclient.discovery

from instance import wait_for_operation


def get_instance(compute, instance_id, project, zone):
    result = compute.instances().get(project=project, zone=zone, instance=instance_id).execute()
    print(result)
    sys.exit()
    #>>> bar['networkInterfaces'][0]['accessConfigs'][0]['natIP']

    return result['items'] if 'items' in result else None
    
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

    #detach_disk(compute, "wes-develop", "wes-auto-disk", project="cidc-biofx", zone='us-east1-b')
    #get_instance(compute, "wes-auto-test", project="cidc-biofx", zone='us-east1-b')
    get_instance(compute, "7690556657012162119", project="cidc-biofx", zone='us-east1-b')
if __name__=='__main__':
    main()

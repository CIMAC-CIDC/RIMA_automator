#!/usr/bin/env python

import os
import sys
import json
import time
import subprocess
from optparse import OptionParser
from datetime import datetime, timedelta

import paramiko
from paramiko import client

###############################################################################
# SSH client class
# ref: https://daanlenaerts.com/blog/2016/01/02/python-and-ssh-sending-commands-over-ssh-using-paramiko/
###############################################################################
class ssh:
    client = None

    def __init__(self, address, username, key_filename):
        # Let the user know we're connecting to the server
        print("Connecting to server.")
        # Create a new SSH client
        self.client = client.SSHClient()
        # The following line is required if you want the script to be able to access a server that's not yet in the known_hosts file
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        # Make the connection
        self.client.connect(address, username=username, key_filename=key_filename, look_for_keys=False)

    def sendCommand(self, command):
        # Check if connection is made previously
        #ref: https://www.programcreek.com/python/example/7495/paramiko.SSHException
        #example 3
        if(self.client):
            status = 0
            try:
                t = self.client.exec_command(command)
            except paramiko.SSHException:
                status=1

            std_out = t[1].read()
            std_err = t[2].read()
            t[0].close()
            t[1].close()
            t[2].close()
            return (status, std_out, std_err)

            # stdin, stdout, stderr = self.client.exec_command(command)
            # while not stdout.channel.exit_status_ready():
            #     if stderr.channel.recv_ready(): 
            #         # Retrieve the first 1024 bytes
            #         alldata = stdout.channel.recv(1024)
            #         print("error")
            #         while stdout.channel.recv_ready():
            #             # Retrieve the next 1024 bytes
            #             alldata += stdout.channel.recv(1024)
                        
            #         # Print as string with utf8 encoding
            #         print(str(alldata, "utf8"))
            #         #DELAY before returning
            #         time.sleep(3)

            #     # Print stdout data when available
            #     if stdout.channel.recv_ready():
            #         print("out")
            #         # Retrieve the first 1024 bytes
            #         alldata = stdout.channel.recv(1024)
            #         while stdout.channel.recv_ready():
            #             # Retrieve the next 1024 bytes
            #             alldata += stdout.channel.recv(1024)
                        
            #         # Print as string with utf8 encoding
            #         print(str(alldata, "utf8"))
            #         #DELAY before returning
            #         time.sleep(3)
        else:
            print("Connection not opened.")
###############################################################################

def main():
    usage = "USAGE: %prog -i [ip addr] -u [user] -k [key]"
    optparser = OptionParser(usage=usage)
    optparser.add_option("-i", "--ip", help="instance ip address")
    optparser.add_option("-u", "--user", help="username")
    optparser.add_option("-k", "--key_file", help="key file path")
    (options, args) = optparser.parse_args(sys.argv)

    if (not options.ip or not options.user or not options.key_file):
        optparser.print_help()
        sys.exit(-1)

    #try to establish a connection
    connection = ssh(options.ip, options.user, options.key_file)
    gs_path="gs://lens_bucket2/wes/speed_tests/mutsig/out.log"    
    print("Downloading raw files...")
    (status, stdin, stderr) = connection.sendCommand("/home/taing/utils/dnldBucket.sh %s %s" % (gs_path, "/mnt/ssd/wes/data"))
    #if stderr:
    #    print(stderr)


if __name__=='__main__':
    main()

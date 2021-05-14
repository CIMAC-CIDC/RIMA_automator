#!/usr/bin/env python
"""Len Taing 2021 (TGBTG)
WES automator config file processor
Problem: we're manually tailoring wes automator config files that come from 
the software team to add things like commit string, wes image, etc.
"""

import os
import sys
import time
from optparse import OptionParser

import ruamel.yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString

def main():
    usage = "USAGE: %prog -c [cores] -d [disk size] -l [cimac center] -s [somatic_caller] -b [google bucket path] -w [wes_commit] -i [wes_image] -r [wes_ref_snapshot] -t [trim_soft_clip]"
    optparser = OptionParser(usage=usage)
    optparser.add_option("-l", "--cimac_center", help="cimac center")
    optparser.add_option("-b", "--google_bucket_path", help="google bucket path")
    optparser.add_option("-w", "--wes_commit", help="wes commit string")
    optparser.add_option("-i", "--image", help="wes image")
    optparser.add_option("-r", "--wes_ref_snapshot", help="wes reference snapshot")

    optparser.add_option("-c", "--cores", help="num. cores (default: 64)", default=64)
    optparser.add_option("-d", "--disk_size", help="disk size in GiB (default: 500)", default=500)
    optparser.add_option("-s", "--somatic_caller", help="somatic_caller (default: tnscope)", default="tnscope")

    optparser.add_option("-t", "--trim_soft_clip", help="trim soft clip (default: false", action="store_true", default=False)
    optparser.add_option("-f", "--directory", help="directory (default: '.')", default=".")
    (options, args) = optparser.parse_args(sys.argv)
    #Convert options to a dictionary
    #ref: https://stackoverflow.com/questions/1753460/python-optparse-values-instance
    options_dict = vars(options)

    if not options.cimac_center or not options.google_bucket_path or not options.wes_commit or not options.image or not options.wes_ref_snapshot:
        print("\nERROR: Please define cimac_center, google_bucket_path, wes_commit, image, and wes_ref_snapshot.  These are required fields.\n")
        optparser.print_help()
        sys.exit(-1)

    files = [f for f in os.listdir(options.directory) if f.endswith('.yaml')]
    #print(options_dict)
    #print(files)

    #remove directory from the list
    config_dir = options.directory
    del options_dict['directory']

    for f in files:
        # PARSE the yaml file
        config_f = open(os.path.join(config_dir, f))
        config = ruamel.yaml.round_trip_load(config_f.read())
        config_f.close()

        #override the params
        for (k,v) in options_dict.items():
            #direct values, e.g. ints, bools
            if k == 'cores' or k == 'disk_size' or k == 'trim_soft_clip':
                config[k] = v
            else: #put it string in quotes
                #ref: https://stackoverflow.com/questions/39262556/preserve-quotes-and-also-add-data-with-quotes-in-ruamel
                config[k] = SingleQuotedScalarString(v)

        #special case for google_bucket, which is in the form of
        #assume that the name of the file is the CIMAC ID
        #otherwise we can use config['instance_name'] or 
        #config['samples']['tumor']
        iid = ".".join(f.split(".")[:-1])
        #remove 'processed' from the name, just in case we re-ran
        iid = iid.replace("_processed", "")
        bucket = options.google_bucket_path.replace("{CIMAC_ID}", iid)
        config['google_bucket_path'] = bucket

        #write new config
        new_fname = "%s_processed.yaml" % iid
        #print(new_fname)
        out = open(os.path.join(config_dir, new_fname), "w")
        ruamel.yaml.round_trip_dump(config, out)
        out.close()

if __name__=='__main__':
    main()


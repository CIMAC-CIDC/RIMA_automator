#!/usr/bin/env python

import os
import sys
import yaml


def main():
    # Read YAML file
    #ref: https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
    with open("automator_config.yaml", 'r') as stream:
        config = yaml.load(stream)

    print(config)
    print(config.keys())

if __name__=='__main__':
    main()

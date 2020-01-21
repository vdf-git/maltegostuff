#!/usr/bin/env python3
import json
import random
import subprocess


'''
gets some random json posts.
'''

def get_post():
    filelist = subprocess.check_output(['find', '../../posts/', '-type', 'f']).decode().split('\n')[:-1]
    nfiles = len(filelist)
    infile = open(filelist[int(random.random() * nfiles)], 'rb')
    myjson = json.loads(infile.read())
    return myjson


def test():
    print(get_post())


if __name__ == "__main__":
    test()

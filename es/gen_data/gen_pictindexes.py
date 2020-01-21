#!/usr/bin/env python3
import random
import re
import subprocess

from elasticsearch import Elasticsearch
import argparse

'''
creates an index of images, containing md5s and paths
also, creates and erdos graph, simulating victimID
'''


def main():
    es = Elasticsearch()

    parser = argparse.ArgumentParser()
    parser.add_argument('--pictlib', dest='pictlib', required=True)
    parser.add_argument('--simprob', dest='simprob', default='0.01')
    args = parser.parse_args()

    prob = float(args.simprob)

    immap = {'mappings': {'image': {'properties': {'path': {'type': 'keyword'}, 'md5': {'type': 'keyword'}}}}}
    try:
        es.indices.delete('images')
    except:
        pass
    es.indices.create('images', body=immap)

    simmap = {'mappings': {'samevict': {'properties': {'md5s': {'type': 'keyword'}}}}}
    try:
        es.indices.delete('samevicts')
    except:
        pass
    es.indices.create('samevicts', body=simmap)

    md5s = []

    md5pat = re.compile(".*/(.*)\\..*")
    imglist = subprocess.check_output(['find', args.pictlib, '-type', 'f']).decode().split('\n')[:-1]
    for impath in imglist:
        m = md5pat.match(impath)
        if not m:
            print("no md5 pat match??? " + impath)
            exit()
        md5s.append(m.group(1))
        image = {'path': impath,
                 'md5': m.group(1)}
        es.index(index='images', doc_type='image', body=image)

    samevicts = dict()
    for image in md5s:
        samevicts[image] = []

    for image in md5s:
        samevicts[image] = []
        counters = md5s[md5s.index(image) + 1:]
        for counter in counters:
            if random.random() < prob:
                samevicts[image].append(counter)
                samevicts[counter].append(image)

    imset = set(md5s)
    while len(list(imset)) > 0:
        victmd5s = {list(imset)[0]}
        prev = set()
        while not victmd5s == prev:
            prev = victmd5s
            for md5 in list(victmd5s):
                for im in samevicts[md5]:
                    victmd5s.add(im)
        for im in victmd5s:
            imset.discard(im)
        vict = {'md5s': list(victmd5s)}
        es.index(index='samevicts', doc_type='samevict', body=vict)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from elasticsearch import Elasticsearch
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='infile', required=True)
    parser.add_argument('--index', dest='index', required=True)
    parser.add_argument('--map', dest='map', required=True)
    args = parser.parse_args()

    es = Elasticsearch()

    try:
        es.indices.delete(index=args.index)
    except Exception:
        pass

    mapfile = open(args.map)
    es.indices.create(index=args.index, body=mapfile.read())

    infile = open(args.infile)
    myid = 0
    for line in infile.readlines():
        myid += 1
        doc = json.loads(line)
        es.create(index=args.index, body=json.dumps(doc), id=myid, doc_type="profile")


if __name__ == "__main__":
    main()

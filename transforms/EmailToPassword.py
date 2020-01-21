#!/usr/bin/env python3

from utils.MaltegoTransform import *
import sys
from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch()
    me = MaltegoTransform()
    email = sys.argv[1]
    bodyquery = {"query": {"match": {"email": email}}}
    res = es.search(index='leaks', body=bodyquery)
    myf = open('/tmp/testout', 'w')
    myf.write(str(bodyquery))
    myf.close()
    for hit in res['hits']['hits']:
        me.addEntity('catlove.password', hit['_source']['password'])
    me.returnOutput()


if __name__ == "__main__":
    main()

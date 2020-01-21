#!/usr/bin/env python3

from utils.MaltegoTransform import *
import sys
from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch()
    me = MaltegoTransform()
    password = sys.argv[1]
    bodyquery = {"query": {"match": {"password": password}}}
    res = es.search(index='leaks', body=bodyquery)
    for hit in res['hits']['hits']:
        me.addEntity('catlove.emailaddress', hit['_source']['email'])
    me.returnOutput()


if __name__ == "__main__":
    main()

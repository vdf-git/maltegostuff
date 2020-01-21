#!/usr/bin/env python3

import argparse
from elasticsearch import Elasticsearch
import random
from utils.get_post import get_post

'''
generates index of private messages from and to users on boards, previously made by gen_profiles
'''


def main():
    es = Elasticsearch()
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapname', dest='mapname', default='privmsgs')
    args = parser.parse_args()
    map = {'mappings': {'privmesg': {'properties': {'sender': {'type': 'keyword'}, 'boardname': {'type': 'keyword'},
                                                    'resceiver': {'type': 'keyword'}, 'message': {'type': 'text'},
                                                    'subject': {'type': 'text'}}}}}

    try:
        es.indices.delete(args.mapname)
    except:
        pass

    es.indices.create(args.mapname, body=map)

    boards = ['Miauland', 'catlove', 'KittyTalk', 'LitterBox', 'catvidz']

    for msn in range(100):
        board = boards[int(random.random() * 5)]
        sender_search = es.search(index='profiles', doc_type='profile', body={
            'query': {'bool': {'must': [{'match': {'board': board}}, {'function_score': {'random_score': {}}}]}}},
                                  size=1000)
        replies = len(sender_search['hits']['hits'])
        sender = sender_search['hits']['hits'][int(random.random() * replies)]['_source']
        receiver_search = es.search(index='profiles', doc_type='profile', body={
            'query': {'bool': {'must': [{'match': {'board': board}}, {'function_score': {'random_score': {}}}]}}},
                                    size=1000)
        replies = len(sender_search['hits']['hits'])
        receiver = receiver_search['hits']['hits'][int(random.random() * replies)]['_source']
        data = get_post()
        privmesg = {'subject': data['subject'],
                    'boardname': board,
                    'body': data['text'],
                    'sender': sender['username'],
                    'receiver': receiver['username']}
        es.index(index=args.mapname, doc_type='privmesg', body=privmesg)


if __name__ == "__main__":
    main()

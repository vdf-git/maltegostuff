#!/usr/bin/env python3

import argparse
from elasticsearch import Elasticsearch
import random
from utils.utils import make_pass, make_username

'''
creates random usernames on random boards, with random passwords
'''


def main():
    es = Elasticsearch()
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapname', dest='mapname', default='profiles')
    args = parser.parse_args()
    mapping = {'mappings': {'profile': {'properties': {'username': {'type': 'keyword'}, 'boardname': {'type': 'keyword'},
                                                       'password': {'type': 'keyword'}}}}}

    try:
        es.indices.delete(args.mapname)
    except:
        pass

    es.indices.create(args.mapname, body=mapping)

    boards = ['Miauland', 'catlove', 'KittyTalk', 'LitterBox', 'catvidz']
    passatoms = ['Ah', 'Le', 'Ma', 'Lu', 'Miau', 'Cat', '123', '54', 'Gollum', 'hood']
    nameadjective = ['tangential', 'mertiticous', 'upright', 'sloppy', 'mischievous', 'sudden', 'feline', 'lazy']
    nameverb = ['stalling', 'marking', 'licking', 'fooling', 'walking', 'trying', 'loving', 'hating']
    namenoun = ['doghater', 'catlady', 'feline', 'catlord', 'mousehunter', 'pussycat', 'jazzcat', 'swingcat']

    for realuser in range(40):
        nprof = int(1 + random.random() * 3)
        normalName = make_username(nameadjective, nameverb, namenoun)
        password = ""
        userboards = set()

        password = make_pass(passatoms, 3)
        for i in range(3):
            password += passatoms[int(random.random() * 10)]
        for prof in range(nprof):
            if random.random() < 0.5:
                name = normalName
            else:
                name = make_username(nameadjective, namenoun, namenoun)
            board = boards[int(random.random() * 5)]
            while (board in userboards):
                board = boards[int(random.random() * 5)]
            userboards.add(board)
            es.index(index=args.mapname, doc_type='profile',
                     body={'username': name, 'board': board, 'password': password})


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import random
from utils.get_post import get_post

'''
generate posts in threads on boards, using profiles created by gen_profiles, sometimes containing pictures defined in
gen_pictindexes.
'''


def main():
    es = Elasticsearch()
    parser = argparse.ArgumentParser()
    parser.add_argument('--nrposts', dest='nrposts', default='10000')
    args = parser.parse_args()

    nrposts = int(args.nrposts)

    postmap = {'mappings': {'post': {'properties': {'poster': {'type': 'keyword'}, 'boardname': {'type': 'keyword'},
                                                    'thread': {'type': 'keyword'}, 'post': {'type': 'text'},
                                                    'subject': {'type': 'text'}, 'images': {'type': 'keyword'}}}}}

    try:
        es.indices.delete('posts')
    except:
        pass

    es.indices.create('posts', body=postmap)

    boards = ['Miauland', 'catlove', 'KittyTalk', 'LitterBox', 'catvidz']

    forums = ['videos', 'photos']
    subforums = ['funny cats', 'beautiful cats']

    users = dict()
    for b in boards:
        users[b] = []

    # get the users on boards profiles
    sciter = scan(es, index='profiles', query={'query': {'match_all': {}}}, scroll='2m', size=1000)
    for p in sciter:
        users[p['_source']['board']].append(p['_source']['username'])

    images = []

    # get the users on boards profiles
    imiter = scan(es, index='images', query={'query': {'match_all': {}}}, scroll='2m', size=1000)
    for p in imiter:
        images.append(p['_source']['md5'])

    for j in range(nrposts):
        b = boards[int(random.random() * len(boards))]
        u = users[b][int(len(users[b]) * random.random())]
        pjson = get_post()
        p = pjson['text']
        s = pjson['subject']
        t = forums[int(len(forums) * random.random())] + '/' + subforums[int(len(subforums) * random.random())]
        i = []
        while random.random() < 0.1:
            i.append(images[int(len(images) * random.random())])
        es.index(index='posts', doc_type='post', body={'poster': u, 'boardname': b, 'post': p, 'subject': s, 'thread': t, 'images': i})


if __name__ == '__main__':
    main()

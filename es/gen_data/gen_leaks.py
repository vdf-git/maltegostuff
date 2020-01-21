#!/usr/bin/env python3

import argparse
import random

'''
"filter": {
    "email": {
        "type": "pattern_capture",
        "preserve_original": "false",
        "patterns": ["([^@]+)"]
    }
},
'''
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from utils.utils import make_username, make_pass

'''
generate a simulacrum of the leaks database with only emails and passwors
'''


def main():
    es = Elasticsearch()
    parser = argparse.ArgumentParser()
    parser.add_argument('--nrusers', dest='nrusers', default='500')
    args = parser.parse_args()

    nrusers = int(args.nrusers)

    mapping = {
        "settings": {
            "analysis": {
                "filter": {
                    "server_removal_filter": {
                        "type": "predicate_token_filter",
                        "script": {
                            "source": "Debug.explain(token)"
                            # "source": "token.getPosition() == 0"
                        }
                    }
                },
                "tokenizer": {
                    "my_tokenizer": {
                        "type": "pattern",
                        "pattern": "(.*)@.*",
                        "group": 1
                    }
                },
                "analyzer": {
                    "email": {
                        "tokenizer": "my_tokenizer",
                        "filter": [
                            "lowercase",
                            "unique"  # ,
                            # "server_removal_filter"
                        ]
                    },
                    "full_email": {
                        "tokenizer": "uax_url_email",
                        "filter": [
                            "lowercase",
                            "unique"
                        ]
                    }

                }
            }
        },
        'mappings': {
            'user': {
                'properties': {
                    'email': {
                        'type': 'text',
                        'analyzer': 'email',
                        'search_analyzer' : 'email',
                        'fields': {
                            'custom': {
                                'type': 'text',
                                'analyzer': 'email',
                                'search_analyzer' : 'full_email'
                            }
                        }
                    },
                    'password': {
                        'type': 'keyword'
                    }
                }
            }
        }
    }

    try:
        es.indices.delete('leaks')
    except:
        pass

    es.indices.create('leaks', body=mapping)

    servers = ['gmail.com', 'sigaint.com', 'protonmail.com', 'hotmail.com', 'yahoo.com', 'yandex.ru']

    users = set()
    passwds = set()

    passatoms = ['Fry', 'Men', 'Tar', '97', 'Ball', 'Rok', '3376', 'NULL', 'Mus', 'bbyyl']

    nameadjective = ['cool', 'flamy', 'young', 'old', 'new', 'green', 'blue', 'forthright', 'high', 'great']
    nameverb = ['rolling', 'blasting', 'listening', 'fighting', 'resting', 'walking', 'biking', 'driving']
    namenoun = ['guy', 'girl', 'hipster', 'worker', 'pensioner', 'painter', 'carpenter', 'boy', 'girl', 'soldier']

    # get the users and passwords from profiles
    sciter = scan(es, index='profiles', query={'query': {'match_all': {}}}, scroll='2m', size=1000)
    for p in sciter:
        users.add(p['_source']['username'])
        passwds.add(p['_source']['password'])

    leaks = []

    for i in range(nrusers):
        if random.random() < 0.05:
            thisusername = list(users)[int(len(users) * random.random())]
        else:
            thisusername = make_username(nameadjective, nameverb, namenoun)
            users.add(thisusername)
        if random.random() < 0.05:
            thispass = list(passwds)[int(len(passwds) * random.random())]
        else:
            thispass = make_pass(passatoms, 3)
            passwds.add(thispass)
        thisemail = thisusername + '@' + servers[int(random.random() * len(servers))]
        leaks.append({'email': thisemail, 'password': thispass})

    for leak in leaks:
        es.index(index='leaks', doc_type='user', body=leak)


if __name__ == "__main__":
    main()

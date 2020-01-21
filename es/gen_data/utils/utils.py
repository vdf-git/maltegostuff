#!/usr/bin/env python3
import random


def make_pass(passatoms, length):
    passwd = ''
    for i in range(length):
        passwd += passatoms[int(len(passatoms) * random.random())]
    return passwd


def make_username(adj, verb, noun):
    username = adj[int(len(adj) * random.random())] + '_' + verb[int(len(verb) * random.random())] + '_' + noun[
        int(len(noun) * random.random())]
    return username

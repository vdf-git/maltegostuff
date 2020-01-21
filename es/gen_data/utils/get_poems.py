#!/usr/bin/env python3

import requests
import json
import hashlib


'''
gets some random poems.
TODO: Understand what for?
'''

def main():
    for i in range(2000):
        r = requests.get(url='https://www.poemist.com/api/v1/randompoems')
        try:
            myjson = json.loads(r.content.decode())
        except:
            continue
        for poem in myjson:
            output = dict()
            output['subject'] = poem['title']
            output['text'] = poem['content']
            to_write = json.dumps(output).encode()
            m = hashlib.md5()
            m.update(to_write)
            filename = m.hexdigest()+'.json'
            outfile = open('/home/vdf/maltego_fun/posts/'+filename, 'wb')
            outfile.write(to_write)
            outfile.close()


if __name__=="__main__":
    main()
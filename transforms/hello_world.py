#!/usr/bin/env python3

from utils.MaltegoTransform import *

def main():
    me = MaltegoTransform()
    me.addEntity("maltego.Phrase", "hello world")
    me.returnOutput()

if __name__=="__main__":
    main()

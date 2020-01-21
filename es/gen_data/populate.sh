#!/bin/bash

./gen_profiles.py
./gen_pictindexes.py --pictlib ../../picts/
./gen_privmsgs.py
./gen_leaks.py
./gen_threadposts.py

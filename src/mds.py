#!/usr/bin/env python3

import argparse
import json
import locale
import os
import shlex
import subprocess
import sys

import jsonavu

def populate_avu(collection,
                 avu):
    """
    performs an 
    'imeta add -C <collection namce> <avu triplet>' call

    expects:
      @input collection - the irods collection
      @input avu        - an avu triplet (dict)
    """
    call = 'imeta add -C {collection} {avu[a]} {avu[v]} {avu[u]}'.format(collection=collection,
     avu=avu)
    call = shlex.split(call)
    process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode(locale.getdefaultlocale()[1])
    err = err.decode(locale.getdefaultlocale()[1])
    if process.returncode == 4:
        print("ERROR: refusing to overwrite existing avu: %s" % avu,
              file=sys.stderr)
    elif process.returncode:
        print("call failed, call was: %s" % ' '.join(call))
        print("Message was: %s" % str(out))
        print("Error code was %s, stderr: %s" % (process.returncode, err))
    return process.returncode, out, err

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    infiles = parser.add_argument_group('Defining input Files')
    infiles.add_argument('-j', '--json', help="defines json schema input")
    
    irods = parser.add_argument_group('iRODs related Information')
    irods.add_argument('-c', '--collection', help="the iRODS collection to annotate")
    
    args = parser.parse_args()

    # load the data
    if os.path.exists(args.json):
       with open(args.json) as fname:
           data = json.load(fname)
    else:
       raise IOError("JSON file '%s' not found" % args.json)

    avus  = jsonavu.json2avu(data, 'root')

    for triplet in avus:
        populate_avu(args.collection,
                     triplet)






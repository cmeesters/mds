#!/usr/bin/env python3

import argparse
import json
import locale
import os
import shlex
import subprocess
import sys

import jsonavu

from metadata import create_data_object_from_json
from nanopub_handler import create_nanopub, set_debug


def populate_avu(collection, avu):
    """
    performs an
    'imeta add -C <collection namce> <avu triplet>' call

    expects:
      @input collection - the irods collection
      @input avu        - an avu triplet (dict)
    """
    call = "imeta add -C {collection} {avu[a]} {avu[v]} {avu[u]}".format(
        collection=collection, avu=avu
    )
    call = shlex.split(call)
    process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode(locale.getdefaultlocale()[1])
    err = err.decode(locale.getdefaultlocale()[1])
    if process.returncode == 4:
        print("ERROR: refusing to overwrite existing avu: %s" % avu, file=sys.stderr)
    elif process.returncode:
        print("call failed, call was: %s" % " ".join(call))
        print("Message was: %s" % str(out))
        print("Error code was %s, stderr: %s" % (process.returncode, err))
    return process.returncode, out, err


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    infiles = parser.add_argument_group("Defining input Files")
    infiles.add_argument("-j", "--json", help="defines json schema input")

    nanopub = parser.add_argument_group("Nanopublication related Information")
    nanopub.add_argument(
        "--real",
        action="store_true",
        help="do not use the nanopub testnet",
        default=False,
    )
    nanopub.add_argument(
        "-n", "--nanopub", action="store_true", help="create a nanopub"
    )

    irods = parser.add_argument_group("iRODs related Information")
    irods.add_argument("-c", "--collection", help="the iRODS collection to annotate")

    utils = parser.add_argument_group("Utility options")
    utils.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="enable debugging output",
        default=False,
    )

    args = parser.parse_args()

    if args.debug:
        set_debug(True)

    data_object = create_data_object_from_json(args.json)
    # print(data_object)
    # sys.exit(0)

    # avus = jsonavu.json2avu(data, "root")

    if args.nanopub:
        create_nanopub(data_object, use_testnet=not args.real, debug_flag=args.debug)


#    for triplet in avus:
#        populate_avu(args.collection, triplet)

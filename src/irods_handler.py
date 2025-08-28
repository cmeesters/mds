import locale
import shlex
import subprocess
import sys


def populate_avu(collection, avu):
    """
    performs an
    'imeta add -C <collection namce> <avu triplet>' call

    expects:
      @input collection - path to the irods collection
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


def get_avus(collection):
    """
    performs an
    'imeta ls -C <collection name>' call

    expects:
      @input collection - path to the irods collection

    returns:
      a list of avu triplets (dicts)
    """

    call = "imeta ls -C {collection}".format(collection=collection)
    call = shlex.split(call)
    process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode(locale.getdefaultlocale()[1])  # decode byte string
    err = err.decode(locale.getdefaultlocale()[1])  # decode byte string
    if process.returncode:
        print("call failed, call was: %s" % " ".join(call))
        print("Message was: %s" % str(out))
        print("Error code was %s, stderr: %s" % (process.returncode, err))
        return process.returncode, [], err  # return empty list on error
    return (
        0,
        [dict(zip(["a", "v", "u"], line.split())) for line in out.splitlines()],
        None,
    )

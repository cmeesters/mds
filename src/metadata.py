import os
import json


def create_data_object_from_json(json_fname):
    """
    Create a data object from a JSON file.

    :param json_fname: The path to the JSON file.
    :return: The data object created from the JSON file.
    """
    # load the data
    if os.path.exists(json_fname):
        with open(json_fname) as fname:
            data = json.load(fname)
    else:
        raise IOError("JSON file '%s' not found" % json_fname)
    return data

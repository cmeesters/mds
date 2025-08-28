import json
import rdflib
from nanopub import Nanopub, NanopubConf, load_profile
import sys

import requests

original_post = requests.post

# Global debug flag - will be set by calling module
debug = False

def set_debug(debug_flag):
    """Set the global debug flag and configure debug hooks if needed."""

    if debug_flag:
        def debug_post(url, *args, **kwargs):
            print(f"\n--- Sending POST to {url} ---")
            if 'json' in kwargs:
                print("JSON payload:", kwargs['json'])
            elif 'data' in kwargs:
                print("Data payload:", kwargs['data'])
            print("---------------------------\n")
        
            return original_post(url, *args, **kwargs)

        requests.post = debug_post


def json2graph(data):
    """ Convert JSON data to an RDF graph.
    :param data: The JSON data to convert.
    :return: An rdflib Graph object.
    """
    g = rdflib.Graph()
    
    # Add some namespace prefixes for better readability
    g.bind("schema", "http://schema.org/")
    g.bind("dct", "http://purl.org/dc/terms/")
    
    if isinstance(data, dict):
        data = json.dumps(data)
    g.parse(data=data.encode('utf-8'), format='json-ld')

    return g

def create_nanopub(data, use_testnet=False, debug_flag=False):
    """
    Create a nanopublication from the given data.

    :param data: The data to be included in the nanopublication.
    :param use_testnet: Boolean indicating whether to use the testnet.
    :return: The URI of the created nanopublication.
    """
    np_conf = NanopubConf(
        use_test_server=use_testnet,
        profile=load_profile(), # Loads the user profile that was created with `np setup`
        add_prov_generated_time=True,
        attribute_publication_to_profile=True,
    )

    # create the assertion graph from JSON data
    g = json2graph(data)
    #try:
    np = Nanopub(
      conf=np_conf,
      assertion=g
    )
    if debug_flag: 
        print("=====")
        print("Assertion graph as TTL:")
        print(g.serialize(format="turtle"))
        print("=====")
        print("\nAssertion graph as JSON-LD:")
        print(g.serialize(format="json-ld"))
        print("=====")
    #np.sign()
    np.publish()
    #except NanopubError as e:
    #    print(f"Error creating nanopublication: {e}")
    #    return None

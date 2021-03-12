#!/usr/bin/env python3

#from setuptools import setup
from distutils.core import setup
import glob
import os

def getfilelist(directory):
    """
    needed to retrieve files recursively of one directory
    """
    # create a list of file and sub directories
    # names in the given directory
    listoffiles = os.listdir(directory)
    allFiles = list()
    # Iterate over all the entries
    for entry in listoffiles:
        # Create full path
        fullpath = os.path.join(directory, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullpath):
            allFiles = allFiles + getfilelist(fullpath)
        else:
            allFiles.append(fullpath)

    return allFiles

setup(name='imcs',
      version='0.1',
      author='Christian Meesters',
      author_email='meesters@uni-mainz.de',
      url='https://gitlab.rlp.net/hpc/imcs',
      # list folders, not files
      #packages=['imcs'],
      scripts=glob.glob('bin/*'),
      data_files=[
                 ('README', 'README'),
                 # ATTENTION: sample data should be small
                 ('sample_data', getfilelist('sample_data'))]
      )

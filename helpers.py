from argparse import ArgumentTypeError
from os.path import exists


def parseInputFile(filepath):
    if not exists(filepath):
        raise ArgumentTypeError('Input file does not exists')
    if not filepath.endswith('.yml'):
        raise ArgumentTypeError('Only .yml file types are currently supported as the input')
    return filepath


def parseBytes32(value):
    as_bytes = None
    try:
        as_bytes = bytes.fromhex(value)
    except:
        raise ArgumentTypeError('Invalid hexadecimal')
    if not len(as_bytes) == 32:
        raise ArgumentTypeError('Invalid length of the hash')
    return as_bytes



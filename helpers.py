from argparse import ArgumentTypeError
from os.path import exists

import re
import requests


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


def fetchTXData(txid):
    url = 'https://www.blockchain.com/btc/tx/{0}'.format(txid)
    print(url)
    r = requests.get(url)
    # get the address
    pattern = r'(?<=<a href\=\"\/btc\/address\/)[A-Za-z0-9]*(?=\")'
    res = re.search(pattern, r.text)
    address = res.group()
    # get the op-return
    pattern = r'(?<=OP_RETURN\<\/span\>\<span\ class\=\"sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC\"\ opacity\=\"1\"\>)[A-Za-z0-9]*(?=\<\/span\>)'
    res = re.search(pattern, r.text)
    op_return = res.group()
    return address, op_return


def decoderOpReturnTrezor(data):
    value = ''
    if int(len(data)/2) != 64:
        raise ValueError('invalid op return for Trezor encoding')
    for j in range(int(len(data)/2)):
        delta = 0
        nb = int(data[2*j]+data[2*j+1])
        if 48 <= nb+18 <= 57:
            delta = 18
        else:
            delta = 4
        txt = str(chr(nb+delta))
        value += txt
    return parseBytes32(value)

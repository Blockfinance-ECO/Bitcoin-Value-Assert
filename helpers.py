import qrcode

from argparse import ArgumentTypeError
from os.path import exists
from PIL import Image

import re
import requests

# brew install zbar
# sudo apt-get install libzbar0
# python -m pip install pyzbar

from pyzbar.pyzbar import decode as dec

def parseInputFile(filepath):
    if not exists(filepath):
        raise ArgumentTypeError('Input file does not exists')
    if not filepath.endswith('.yml'):
        raise ArgumentTypeError('Only .yml file types are currently supported as the input')
    return filepath


def parseQRFile(filepath):
    if not filepath.endswith('.png'):
        raise ArgumentTypeError('Only .png file types are currently supported as the type of file')
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


def makeQRCode(txid: bytes, key: bytes, message: str, filename: str):
    data = txid.hex() + key.hex() + message

    QR = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    QR.add_data(data)
    QR.make(fit=True)
    image = QR.make_image(fill_color="black", back_color="white")
    image.save(filename)


def parseQRCode(filename: str):
    decoded = dec(Image.open(filename))
    data = decoded[0][0]

    txid = parseBytes32(data[0:64].decode())
    key = parseBytes32(data[64:128].decode())
    message = data[128:].decode()

    return txid, key, message

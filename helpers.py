import qrcode
import textwrap

from argparse import ArgumentTypeError
from os.path import exists
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

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

def parseOutputFile(filepath):
    if exists(filepath):
        raise ArgumentTypeError('Output file does already exist')
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


def fetchTXMainnetData(txid):
    url = 'https://www.blockchain.com/btc/tx/{0}'.format(txid)
    print('fetching...', url)
    print()
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


def fetchTXData(txid):
    url = 'https://www.blockchain.com/btc-testnet/tx/{0}'.format(txid)
    print('fetching...', url)
    print()
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # get the address
    els = soup.select('#__next > div.sc-1udt3q6-0.irpFhx > div.sc-1udt3q6-1.ijayGs > div > div > div:nth-child(5) > div > div:nth-child(3) > div:nth-child(2) > div.odi4cq-0.gVJWcr > div.ccso3i-0.dJDEkx > div > a')
    if len(els) == 0:
        raise Exception('Could not fetch the BTC testnet address')
    address = els[0].text
    # get the op-return
    els = soup.select('#__next > div.sc-1udt3q6-0.irpFhx > div.sc-1udt3q6-1.ijayGs > div > div > div:nth-child(5) > div > div:nth-child(2) > div:nth-child(3) > div > div.ccso3i-0.dJDEkx > div > span:nth-child(2)')
    if len(els) == 0:
        raise Exception('Could not fetch the op_return code')
    op_return = els[0].text
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


def renderMessageAsImage(message, width, height):
    wrapper = textwrap.TextWrapper(width=16)
    lines = wrapper.wrap(text=message)
    margin = 10
    nb_lines = len(lines)
    wrapped_message = '\n'.join(lines)
    font = ImageFont.truetype('fonts/monoMMM_5.ttf', 19)
    font_width, font_height = font.getsize(wrapped_message)
    txt = Image.new('RGB', (width, font_height*nb_lines + margin), 'white')
    draw = ImageDraw.Draw(txt)
    draw.text((2*margin, margin), wrapped_message, font=font, fill='black')
    return txt


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
    width, height = image.size

    image_msg = renderMessageAsImage(message, width, height)
    w2, h2 = image_msg.size

    img2 = Image.new("RGB", (width, height + h2), 'white')
    img2.paste(image_msg, (0, 0))
    img2.paste(image, (0, h2))
    img2.save(filename)


def parseQRCode(filename: str):
    decoded = dec(Image.open(filename))
    data = decoded[0][0]

    txid = parseBytes32(data[0:64].decode())
    key = parseBytes32(data[64:128].decode())
    message = data[128:].decode()

    return txid, key, message

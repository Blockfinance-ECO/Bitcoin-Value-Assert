import argparse
import pathlib

from helpers import parseQRFile, parseQRCode, fetchTXData, decoderOpReturnTrezor
from bva import verify


parser = argparse.ArgumentParser(
    description='Bitcoin Value Assert Proof of Concept')

parser.add_argument('qr_code_file',
                    type=lambda x: parseQRFile(x),
                    help='Output image file for the QR code')

args = parser.parse_args()
txid, _key, message = parseQRCode(args.qr_code_file)

txid = txid.hex()

bitcoin_address, op_return = fetchTXData(txid)

print(bitcoin_address)
print(message)

bitcoin_address = bytes(bitcoin_address, 'utf-8')

_hash = decoderOpReturnTrezor(op_return)

# run the verification
verify(_key, bitcoin_address, message, _hash)
print()
print('valid!')

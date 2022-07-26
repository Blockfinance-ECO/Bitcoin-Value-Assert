import argparse
import pathlib
import yaml

from helpers import makeQRCode, parseInputFile, parseQRFile, parseBytes32

parser = argparse.ArgumentParser(
    description='Bitcoin Value Assert Proof of Concept')
parser.add_argument('input',
                    type=lambda x: parseInputFile(x),
                    help='File containing the verification data')
parser.add_argument('qr_code_file',
                    type=lambda x: parseQRFile(x),
                    help='Output image file for the QR code')
args = parser.parse_args()

# parse the input file and extract the variables
input_file = None
with open(args.input) as f:
    input_file = yaml.load(f, Loader=yaml.FullLoader)

txid = parseBytes32(input_file['txid'])
message = input_file['message'] # bytes(input_file['message'], 'utf-8')
_key = parseBytes32(input_file['key'])

makeQRCode(txid, _key, message, args.qr_code_file)

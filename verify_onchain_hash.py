import argparse
import pathlib
import yaml

from helpers import parseInputFile, parseBytes32, fetchTXData, decoderOpReturnTrezor
from bva import verify


parser = argparse.ArgumentParser(
    description='Bitcoin Value Assert Proof of Concept')
parser.add_argument('input',
                    type=lambda x: parseInputFile(x),
                    help='File containing the verification data')
args = parser.parse_args()

# parse the input file and extract the variables
input_file = None
with open(args.input) as f:
    input_file = yaml.load(f, Loader=yaml.FullLoader)

txid = input_file['txid']
message = bytes(input_file['message'], 'utf-8')
_key = parseBytes32(input_file['key'])

bitcoin_address, op_return = fetchTXData(txid)
bitcoin_address = bytes(bitcoin_address, 'utf-8')

_hash = decoderOpReturnTrezor(op_return)

# run the verification
verify(_key, bitcoin_address, message, _hash)
print()
print('valid!')

import argparse
import pathlib
import yaml

from helpers import parseInputFile, parseBytes32
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

# ( normally the bitcoin_address would be taken from the transaction data )
bitcoin_address = bytes(input_file['bitcoin_address'], 'utf-8')

message = bytes(input_file['message'], 'utf-8')
_hash = parseBytes32(input_file['hash'])
_key = parseBytes32(input_file['key'])

# run the verification
verify(_key, bitcoin_address, message, _hash)
print()
print('valid!')

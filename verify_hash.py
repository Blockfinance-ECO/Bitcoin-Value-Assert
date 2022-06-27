import argparse
import pathlib
import yaml

from helpers import parseInputFile, parseBytes32
from bva import verify


parser = argparse.ArgumentParser(
    description='Bitcoin Value Assert Proof of Concept')
parser.add_argument('input',
                    type=lambda x: parseInputFile(x),
                    help='Input file to compute the hash')
parser.add_argument('hash',
                    type=lambda x: parseBytes32(x),
                    help='Hash from the block')
parser.add_argument('key',
                    type=lambda x: parseBytes32(x),
                    help='Derived key from the verification data')
args = parser.parse_args()

# parse the input file and extract the variables
input_file = None
with open(args.input) as f:
    input_file = yaml.load(f, Loader=yaml.FullLoader)

# ( normally the bitcoin_address would be taken from the transaction data )
bitcoin_address = bytes(input_file['bitcoin_address'], 'utf-8')

# ( normally the message would be taken from the verification data )
message = bytes(input_file['message'], 'utf-8')

# run the verification
verify(args.key, bitcoin_address, message, args.hash)
print()
print('valid!')

import argparse
import pathlib
import yaml

from helpers import parseInputFile
from bva import produce

# parse the command line arguments
parser = argparse.ArgumentParser(
    description='Bitcoin Value Assert Proof of Concept')
parser.add_argument('input',
                    type=lambda x: parseInputFile(x),
                    help='Input file to compute the hash')
args = parser.parse_args()

# parse the input file
input_file = None
with open(args.input) as f:
    input_file = yaml.load(f, Loader=yaml.FullLoader)

# extract the variables
bitcoin_address = bytes(input_file['bitcoin_address'], 'utf-8')
message = bytes(input_file['message'], 'utf-8')
application = input_file['application']
timestamp = input_file['timestamp']
purpose = input_file['purpose']
nounce = bytes.fromhex(input_file['nounce'])

# compute the hash
_hash, derived_key = produce(
    bitcoin_address,
    message,
    application,
    timestamp,
    purpose,
    nounce=nounce)

# display the data
print()
print('hash')
print(_hash.hex())
print()
print('derived key')
print(derived_key.hex())

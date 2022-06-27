import secrets

from blake3 import blake3


def computeInputValue(bitcoin_address: bytes, message: bytes):
    # compute the bitcoin_address_hash
    bitcoin_address_hash = blake3(bitcoin_address).digest()
    # compute the message hash
    message_hash = blake3(bitcoin_address).digest()
    # compute the input by concatenating the bitcoin_address_hash
    # with the message hash
    input_value = bitcoin_address_hash + message_hash
    return input_value


# this function produces the hash
def produce(
        bitcoin_address: bytes,
        message: bytes,
        application: str, timestamp: str, purpose: str, nounce=None):
    # compute the input value
    input_value = computeInputValue(bitcoin_address, message)
    # generate the random nounce if needed
    random_nounce = None
    if nounce is None:
        random_nounce = secrets.token_bytes(32)
    else:
        random_nounce = nounce
    # derive the key
    context = application + timestamp + purpose
    derived_key = blake3(random_nounce, derive_key_context=context).digest()
    # compute the hash
    _hash = blake3(input_value, key=derived_key).digest()
    return _hash, derived_key


# this function allows to verify the hash
# from verification data we have
# * derived_key
# * message
# and from transaction data we have
# * bitcoin_address
# from the block
# * _hash
def verify(derived_key: bytes,
           bitcoin_address: bytes,
           message: bytes,
           _hash: bytes):
    # compute the input value
    input_value = computeInputValue(bitcoin_address, message)
    # re-calculate the hash
    recalculated_hash = blake3(input_value, key=derived_key).digest()
    # check if matches
    assert recalculated_hash == _hash

import unittest

from bva import produce


def test_scenario_1():
    bitcoin_address = bytes('1DbibSZzvqhv3c2b8AKq3SgvQGX1pQx6sX', 'utf-8')
    message = bytes('Street 4, Town, 99-999 State, Country', 'utf-8')
    application = 'Application name'
    timestamp = '1656337808'
    purpose = 'government verification'
    nounce = bytes.fromhex('0d209ddd3982274a5203e6d42ef173714aa472192c01641f351a7a23fbfba9f7')
    # compute the hash
    _hash = produce(bitcoin_address, message, application, timestamp, purpose, nounce=nounce)
    assert len(_hash) == 32
    print(_hash)
    #print(bitcoin_address_bytes.hex())
    #assert False


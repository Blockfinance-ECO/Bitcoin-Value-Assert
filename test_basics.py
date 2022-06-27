import unittest

from bva import produce, verify


def test_scenario_1():
    bitcoin_address = bytes('1DbibSZzvqhv3c2b8AKq3SgvQGX1pQx6sX', 'utf-8')
    message = bytes('Street 4, Town, 99-999 State, Country', 'utf-8')
    application = 'Application name'
    timestamp = '1656337808'
    purpose = 'government verification'
    nounce = bytes.fromhex(
        '0d209ddd3982274a5203e6d42ef173714aa472192c01641f351a7a23fbfba9f7')
    # compute the hash
    _hash, derived_key = produce(
        bitcoin_address,
        message,
        application,
        timestamp,
        purpose,
        nounce=nounce)
    # we have some hard-coded data to compare with
    assert _hash == bytes.fromhex(
        'f884e6fd1c328ddf49ab282ec4e647b9532ae91ab23e9307216d2d841ec84782')
    # auto-verify
    verify(derived_key, bitcoin_address, message, _hash)

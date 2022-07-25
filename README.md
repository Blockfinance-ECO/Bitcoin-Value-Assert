# Bitcoin-Value-Assert
Value Assert is a simple on-chain protocol that enters a hash-obscured message into the blockchain that is associated with a particular bitcoin transition. This allows somebody to publicly assert possession of the coins included in this special transaction.

## Abstract
In this specification we define a protocol for making a publicly assertion related to a bitcoin transaction.

## Link
https://gist.github.com/da2ce7/f6ba2d3126d4785951a03149a604a3d7

Bitcoin Improvement Proposals Fork: https://github.com/Hodl10-AG/bips

## Proof of Concept

### Setup

```sh
pip install -r requirements.txt
```

### Preparing the data

Make a `.yml` file like the `example_input.yml`, as follows

```yml
bitcoin_address: "1DbibSZzvqhv3c2b8AKq3SgvQGX1pQx6sX"
message: "Street 4, Town, 99-999 State, Country"
application: "Application name"
timestamp: "1656337808"
purpose: "government verification"
nounce: "0d209ddd3982274a5203e6d42ef173714aa472192c01641f351a7a23fbfba9f7"
```

### Computing the hash

Run the following command

```bash
$ python compute.py example_input.yml 
```

you should get output as follows

```

hash
f884e6fd1c328ddf49ab282ec4e647b9532ae91ab23e9307216d2d841ec84782

derived key
31888d9ff481c498bc353f8624cdb53fe4cb28544078a9b8fa05f06a93107628
```

put this in the `.yml` file containing verification data.

### Verifying the hash

To verify you may run

```bash
$ python verify_onchain_hash.py example_onchain_verification.yml
```

and your response will be

```

valid!
```

however if you tamper with the data like if you slightly change the hash you will get an error indicating the hash mismatch

```
Traceback (most recent call last):
  File "verify_hash.py", line 34, in <module>
    verify(args.key, bitcoin_address, message, args.hash)
  File "/Users/marek/Development/sqrtxx/Bitcoin-Value-Assert/bva.py", line 55, in verify
    assert recalculated_hash == _hash
AssertionError
```

which is a verification failure!

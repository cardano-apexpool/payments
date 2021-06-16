# Cardano Payments

- Implemented in Python3
- Support for Native Tokens

## Requirements:
- cardano-cli (part of [cardano-node](https://github.com/input-output-hk/cardano-node))
- a cardano node running, with the blockchain synchronized ([Daedalus Wallet](https://daedaluswallet.io/en/download/) or [cardano-node](https://github.com/input-output-hk/cardano-node)).
The easiest way is to use the Daedalus Wallet. For Testnet you can use [Daedalus wallet for the Cardano testnet](https://developers.cardano.org/en/testnets/cardano/get-started/wallet/) - this is how I developed and tested the scripts.

The Daedalus Wallet is a full node wallet and it will download the full blockchain (about 2.3 GB for testnet and 8 GB for mainnet for the moment) before it can be used. This could take a couple of hours, depending on your internet connection and your computer.
Be sure to always download the Daedalus Wallet only from trusted sources and to check the sha256 sum before installing it.
After installing and starting it, you can create your own wallet, and you must save the recovery seed (24 words) and set a Spending Password. You will need the recovery seed in case you want to restore the wallet on a different computer 
(or using another software wallet, for example [Yoroi Wallet](https://yoroi-wallet.com/), which is a light wallet). You will need the Spending Password each time you want to make a payment.
For the moment I only tested the scripts in testnet, so I'll be talking about test ADA, but it should be similar for ADA in mainnet. I will update the documentation once I test it in mainnet, too. 
The only difference is in the cardano-cli parameters, the testnet has an extra "magic" number as parameter.

## How to use the scripts:
- First you will need a few signing keys and addresses to play with. You can use the "payment-address.sh" bash script to generate them. You can adjust the script if you want. 
The script will create by default 10 payment keys and 10 payment addresses. The keys will be created in the "keys" subdirectory, and the addresses in the "addresses" subdirectory, if you do not change the paths in the script. 
The "files" subdirectory will also be created, this is where the python scripts will save the "protocol.json" file, required to calculate the transaction fees.
- You can check the amounts of lovelace and native tokens at these addresses using the bash script "query-payment-addresses.sh". If you need test ADA (tADA) and test tokens to play with, 
you can use the [Testnet Faucet](https://developers.cardano.org/en/testnets/cardano/tools/faucet/) to request them. There's a daily limit of 1000 tADA and 2 testcoins, but this will be more than enough to play with. 
You will get an answer like this one:
```
$ . query-payment-addresses.sh  
1 -> addr_test1vpsgc7v2f7yfluephhweddtzcvp4xtufjq0jpkfksrezvzgarjqsu
2 -> addr_test1vrnxsegyl05xfgh50e203mzv230fuvyhky33ce4wzmq0t6gd5stqz
3 -> addr_test1vzag9hr2tdq5ha3sc84gqvj2e7geta55fnjttfa9g5rj8qct05dd0
4 -> addr_test1vryj8llkvcphdku9wcyk67vra8fxynhcj47t6lfvgtu3n7qxlthsf
5 -> addr_test1vz8y7rsrf9pcfaxxqsvkmp0gccku97lrw4x6uajtsm4n2xq6rss0x
6 -> addr_test1vr69x66z9ht98nq9hkdkv7tp9ze5vnnhd2m5usdtk6khkesnmwl4e
7 -> addr_test1vz2jr07lrwf0p8z4xrc32f67tdsf7pzt533yz8ynyse92cgeymsw7
8 -> addr_test1vpekasdmfxzpjr5ryjr4n380lalqg740043j7tpst9lf5mgsznjkp
9 -> addr_test1vr26ld7yrnl653w93s6g4gsnqwgehtajvjxracqp9f4gs5s4v2jet
10 -> addr_test1vpvet74gr3x9u6ydf0lm805mrhlkxgrvw893yfagakkxd2cj9y5ns
```
- If you transfer 1000 tADA and 2 testcoins from the Faucet to the first address in the list, you will get an answer like this one:
```
$ . query-payment-addresses.sh 
1 -> addr_test1vpsgc7v2f7yfluephhweddtzcvp4xtufjq0jpkfksrezvzgarjqsu
83b1ec516bc5d1055d60748217658dc891117d5925f24ff8659edf2a98c9df05     0        1000000000 lovelace + 2 6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7
2 -> addr_test1vrnxsegyl05xfgh50e203mzv230fuvyhky33ce4wzmq0t6gd5stqz
3 -> addr_test1vzag9hr2tdq5ha3sc84gqvj2e7geta55fnjttfa9g5rj8qct05dd0
4 -> addr_test1vryj8llkvcphdku9wcyk67vra8fxynhcj47t6lfvgtu3n7qxlthsf
5 -> addr_test1vz8y7rsrf9pcfaxxqsvkmp0gccku97lrw4x6uajtsm4n2xq6rss0x
6 -> addr_test1vr69x66z9ht98nq9hkdkv7tp9ze5vnnhd2m5usdtk6khkesnmwl4e
7 -> addr_test1vz2jr07lrwf0p8z4xrc32f67tdsf7pzt533yz8ynyse92cgeymsw7
8 -> addr_test1vpekasdmfxzpjr5ryjr4n380lalqg740043j7tpst9lf5mgsznjkp
9 -> addr_test1vr26ld7yrnl653w93s6g4gsnqwgehtajvjxracqp9f4gs5s4v2jet
10 -> addr_test1vpvet74gr3x9u6ydf0lm805mrhlkxgrvw893yfagakkxd2cj9y5ns

```
- Now, that you have 1000 tADA and 2 testcoins, you can use the script to make some payments. 
Unlike a normal wallet, the scripts will allow you to send tADA and testcoins (and other tokens, if you have - I created my own tokens on testnet and also did tests with them) 
to multiple addresses in one transaction. And also, unlike a normal wallet, the scripts will need as input the addresses where your tADA and tokens are, 
in order to use exactly the UTXOs from these addresses as source for your payments.
You have multiple options to configure source addresses, destination addresses and the amounts transferred. This is done by editing the "config.py" file.

1. In case you want to transfer just tADA from one address to another address, you can configure the source address, destination address and amount like this:
```
SRC_ADDRESSES = [ADDRESSES_PATH + '/payment-1.addr']
SRC_KEYS = [KEYS_PATH + '/payment-1.skey']
DST_ADDRESSES = [ADDRESSES_PATH + '/payment-3.addr']
AMOUNTS = [100000000]
```
This means that an amount of 100000000 lovelace (100 tADA) will be transferred from the first address to the third address. 
The amounts of tADA must be specified in lovelace (1 tADA = 1 million lovelace, same for ADA).
We have 1000 tADA at the first address, so we need to do something with the rest of 900 tADA and with the 2 testcoins. 
Using this synthax, the 900 tADA and the 2 testcoins will be send to the address where they were initially, in this case the first address. 

2. In case you want to transfer just tADA from one address to another address, but you also want to transfer the remaining tADA to another address, you can configure the source address, destination addresses and amount like this:
```
SRC_ADDRESSES = [ADDRESSES_PATH + '/payment-1.addr']
SRC_KEYS = [KEYS_PATH + '/payment-1.skey']
DST_ADDRESSES = [ADDRESSES_PATH + '/payment-3.addr', ADDRESSES_PATH + '/payment-6.addr']
AMOUNTS = [100000000]
```
This means that an amount of 100000000 lovelace (100 tADA) will be transferred from the first address to the third address. 
The remaining 900 tADA and 2 testcoins will be transferred to the sixth address (located in the "payment-6.addr" file in the "addresses" subdirectory, if you did not change the paths). 
So, if you configure one destination address more than the number of amounts, it means that the remaining tADA and testcoins (and any other tokens you might have in the source addresses) will be transferred to the last configured address.

You can also specify the amounts like this for the same result:
```
AMOUNTS = [100000000, 0]
```
So, if you configure the same number of destination addresses and amounts to be transferred, but the last amount is 0, it means that the remaining tADA (and tokens) will be transferred to the last destination address.

3. In case you want to transfer just tADA from one address to another address, you can configure this just like in the example before, and specify the amount for each destination address:
```
SRC_ADDRESSES = [ADDRESSES_PATH + '/payment-1.addr']
SRC_KEYS = [KEYS_PATH + '/payment-1.skey']
DST_ADDRESSES = [ADDRESSES_PATH + '/payment-3.addr', ADDRESSES_PATH + '/payment-6.addr']
AMOUNTS = [100000000, 200000000]
```
This means that an amount of 100000000 lovelace (100 tADA) will be transferred from the first address to the third address, and 200000000 lovelace (200 tADA) will be transferred from the first address to the sixth address.
The remaining 700 tADA and 2 testcoins will be transferred in this case to the source address, the first address, just like in the first example.
You can always have more that one source address, just add it to SRC_ADDRESSES list:
```
SRC_ADDRESSES = [ADDRESSES_PATH + '/payment-1.addr', ADDRESSES_PATH + '/payment-2.addr']
SRC_KEYS = [KEYS_PATH + '/payment-1.skey', KEYS_PATH + '/payment-2.skey']
```
You will also have to configure the payment signing key for the second payment address, otherwise the transaction will fail.
The remaining tADA will be transferred in this case to the first source address in the list.

4. In case you want to transfer not only tADA, but also native tokens, you must configure the amounts like this:
```
DST_ADDRESSES = [
    ADDRESSES_PATH + '/payment-5.addr',
    ADDRESSES_PATH + '/payment-7.addr'
]
AMOUNTS = [
    [
        {'token': 'lovelace', 'amount': '10000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '1'}
    ],
    [
        {'token': 'lovelace', 'amount': '30000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '1'}
    ]
]

```
The source address(es) will be configured just like in the previous examples.
In this example, 10 tADA and 1 "testcoin" will be transferred to the 5th address (first destination address), and 30 tADA and 1 testcoin will be transferred to the 7th address (second detination address in the list).
The remaining tADA will (and other tokens you might have) will be transferred to the first source address. If you want them transferred to another address, configure an extra destiation address, like in the second example.
When transferring tokens, you must always include at least 1 tADA in the transaction, otherwise the transaction will fail.

5. You can also send only tADA to one address, and send tADA and other tokens (like testcoins) to another address. You can configure the amounts 2 ways.
First way is this:
```
DST_ADDRESSES = [
    ADDRESSES_PATH + '/payment-5.addr',
    ADDRESSES_PATH + '/payment-7.addr'
]
AMOUNTS = [
    [
        {'token': 'lovelace', 'amount': '10000000'}
    ],
    [
        {'token': 'lovelace', 'amount': '30000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '1'}
    ]
]

```
Second way (easier) is this:
```
DST_ADDRESSES = [
    ADDRESSES_PATH + '/payment-5.addr',
    ADDRESSES_PATH + '/payment-7.addr'
]
AMOUNTS = [
    10000000,
    [
        {'token': 'lovelace', 'amount': '30000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '1'}
    ]
]

```
Both ways will have the same effect: 10 tADA will be transferred to the 5th address (located in the "payment-5.addr" file), and 30 tADA and 1 testcoin will be transferred to the 7th address.
The remaining tADA and 1 testcoin will be transferred to the first source address in the list.
Internally, the scripts will convert all amounts into the first from the 2 formats, before doing any other operation. Even when all the amounts are just numbers (like in the first 2 examples), the scripts are converting the amounts 
into the "{'token': 'lovelace', 'amount': '30000000'}" format. 

Just like mentioned before, if the last amount is 0 (specified as integer: 0 or as dictionary: "{'token': 'lovelace', 'amount': '0'}"), the remaining tADA and other tokens will be transferred to the last destination address in the list.

### Changelog
- 16.06.2021 - Update for running on mainnet, tested with cardano-cli 1.27.0
- 09.04.2021 - Update for compatibility with cardano-cli version 1.26.1
- 27.03.2021 - Bug fixes, validation, tests, Documentation
- 26.03.2021 - Token Transactions
- 20.03.2021 - Update
- 11.03.2021 - First version, compatible with cardano-cli version 1.25.1

#!/usr/bin/env python3

import os

# paths
KEYS_PATH = os.getenv('KEYS_PATH', 'keys')
ADDRESSES_PATH = os.getenv('ADDRESSES_PATH', 'addresses')
FILES_PATH = os.getenv('FILES_PATH', 'files')

# general settings
PROTOCOL_FILE = os.getenv('PROTOCOL_FILE', FILES_PATH + '/protocol.json')
CARDANO_ERA = os.getenv('CARDANO_ERA', 'mary')
CARDANO_NET = os.getenv('CARDANO_NET', '--testnet-magic')
MAGIC_NUMBER = os.getenv('MAGIC_NUMBER', '1097911063')


# payment settings

# source addresses (in individual text files)
# and keys (in individual text files) to sign the transactions
SRC_ADDRESSES = [ADDRESSES_PATH + '/payment-9.addr', ADDRESSES_PATH + '/payment-10.addr']
SRC_KEYS = [KEYS_PATH + '/payment-9.skey', KEYS_PATH + '/payment-10.skey']

# destination addresses (in individual text files)
#
# if the number of destination addresses is equal to the number of amounts
# and the last amount is 0
# or if the number of destination addresses is equal to the number of amounts + 1
# the change will be sent to the last destination address
#
# if the number of destination addresses is equal to the number of amounts
# and the last amount is not 0
# the change will be sent to the first source address
#
# if there is only one destination address and the amount is 0
# all the amounts in the source addresses (minus fee)
# will be sent to the destination address
#
#
DST_ADDRESSES = [ADDRESSES_PATH + '/dev_wallet.addr']
AMOUNTS = [20000000]

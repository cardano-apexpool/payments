from params import *


# payment settings

# source addresses (in individual text files)
# and keys (in individual text files) to sign the transactions

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


# 1
SRC_ADDRESSES = [
    ADDRESSES_PATH + '/payment-1.addr',
    ADDRESSES_PATH + '/payment-2.addr'
]
SRC_KEYS = [
    KEYS_PATH + '/payment-1.skey',
    KEYS_PATH + '/payment-2.skey'
]

DST_ADDRESSES = [
    ADDRESSES_PATH + '/payment-3.addr',
    ADDRESSES_PATH + '/payment-4.addr',
    ADDRESSES_PATH + '/payment-9.addr'
]
AMOUNTS = [
    100000000,
    [
        {'token': 'lovelace', 'amount': '20000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '2'}
    ]
]


"""
# 2
SRC_ADDRESSES = [
    ADDRESSES_PATH + '/payment-3.addr',
    ADDRESSES_PATH + '/payment-4.addr',
    ADDRESSES_PATH + '/payment-9.addr'
]
SRC_KEYS = [
    KEYS_PATH + '/payment-3.skey',
    KEYS_PATH + '/payment-4.skey',
    KEYS_PATH + '/payment-9.skey'
]

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
"""
"""
# 3
SRC_ADDRESSES = [
    ADDRESSES_PATH + '/payment-3.addr',
    ADDRESSES_PATH + '/payment-5.addr',
    ADDRESSES_PATH + '/payment-7.addr'
]
SRC_KEYS = [
    KEYS_PATH + '/payment-3.skey',
    KEYS_PATH + '/payment-5.skey',
    KEYS_PATH + '/payment-7.skey'
]
DST_ADDRESSES = [ADDRESSES_PATH + '/dev_wallet.addr']
AMOUNTS = [0]
"""


"""
#
# other examples
#

DST_ADDRESSES = [ADDRESSES_PATH + '/dev_wallet.addr']
AMOUNTS = [
    [
        {'token': 'lovelace', 'amount': 0}
    ]
]
AMOUNTS = [
    [
        {'token': 'lovelace', 'amount': '15000000'},
        {'token': '542b7ade184b6eea769f42d2d1f2902f366e0e9369b719d671e3d498.apexcoin', 'amount': '500'}
    ],
    [
        {'token': 'lovelace', 'amount': '12000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '2'}
    ],
    [
        {'token': 'lovelace', 'amount': '10000000'},
        {'token': '6b8d07d69639e9413dd637a1a815a7323c69c86abbafb66dbfdb1aa7', 'amount': '1'},
        {'token': '542b7ade184b6eea769f42d2d1f2902f366e0e9369b719d671e3d498.apexcoin', 'amount': '100'}
    ]
]
"""

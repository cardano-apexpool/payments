#!/usr/bin/env python3


"""
Created: 11.03.2021
Updated: 20.03.2021
Updated: 26.03.2021 - Token Transactions
Updated: 27.03.2021 - Bug fixes, validation, tests
"""


import json
from library import *


if __name__ == '__main__':

    # transform lovelace amounts from integers to dictionaries
    amounts, spend_amounts = transform_amounts(AMOUNTS)

    # generate the protocol file
    cmd = ["cardano-cli", "query", "protocol-parameters", CARDANO_NET, str(MAGIC_NUMBER), "--out-file", PROTOCOL_FILE]
    _, _ = cardano_cli_cmd(cmd)

    # query tip
    cmd = ["cardano-cli", "query", "tip", CARDANO_NET, str(MAGIC_NUMBER)]
    out, err = cardano_cli_cmd(cmd)

    # set transaction expire time in TRANSACTION_EXPIRE seconds (default 300)
    expire = json.loads(out)['slot'] + TRANSACTION_EXPIRE

    # get the list of transactions from all source addresses
    src_transactions = []
    src_token_transactions = []
    src_address = ''
    tokens_amounts = {}
    for address in SRC_ADDRESSES:
        try:
            with open(address, 'r') as f:
                src_addr = f.read()
                if src_address == '':
                    # keep the first source address for change, if required
                    src_address = src_addr
        except Exception as err:
            print('Error while opening the file: %s' % err)
            sys.exit(1)
        trans, token_trans, out, err = get_transactions(src_addr, tokens_amounts)
        if err:
            print(err)
            sys.exit(1)
        else:
            src_transactions += trans
            src_token_transactions += token_trans
    # debug
    if len(src_transactions) == 0 and len(src_token_transactions) == 0:
        print('No source transactions (UTXOs)!')
        sys.exit(1)
    # print('Source transactions: %s' % src_transactions)
    # print('Source token transactions: %s' % src_token_transactions)
    # print('Change address (if required): %s' % src_address)
    print('Tokens amounts: %s' % tokens_amounts)
    print("Amounts to spend: %s" % spend_amounts)

    # validate transation
    if not validate_transaction(spend_amounts, tokens_amounts):
        print("Spending more than existing amounts is not possible!")
        sys.exit(1)

    # get the list of destination addresses
    dst_addresses = []
    for address in DST_ADDRESSES:
        try:
            with open(address, 'r') as f:
                dst_addr = f.read()
        except Exception as err:
            print('Error while opening the file: %s' % err)
            sys.exit(1)
        dst_addresses += dst_addr.splitlines()
    # debug
    if len(dst_addresses) == 0:
        print('No destination addresses!')
        sys.exit(1)
    print('Destination addresses: %s\n' % dst_addresses)

    # create draft transaction
    _, err, incount, outcount = create_transaction(src_transactions, src_token_transactions,
                                                           src_address, dst_addresses, 200000, 'tx.draft',
                                                           expire, amounts, tokens_amounts)
    if err:
        print(err)
        sys.exit(1)

    # calculate transaction fee
    out, err = calculate_fee('tx.draft', incount, outcount, len(SRC_KEYS))
    if not err:
        fee = int(out.split()[0])
    else:
        print(err)
        sys.exit(1)
    print('Transaction fee: %s\n' % fee)

    # create transaction
    _, err, incount, outcount = create_transaction(src_transactions, src_token_transactions,
                                                           src_address, dst_addresses, fee, 'tx.raw',
                                                           expire, amounts, tokens_amounts)
    if err:
        print(err)
        sys.exit(1)

    # sign transaction
    _, err = sign_transaction(SRC_KEYS, 'tx.raw', 'tx.signed')
    if err:
        print(err)
        sys.exit(1)

    # ask for confirmation before sending the transaction
    while True:
        reply = input('Confirm? [y/n] ')
        if reply.lower() in ('y', 'yes'):
            cmd = ["cardano-cli", "transaction", "submit", "--tx-file", 'tx.signed', CARDANO_NET, str(MAGIC_NUMBER)]
            # submit transaction
            out, err = cardano_cli_cmd(cmd)
            if err:
                print(err)
                sys.exit(1)
            print('Transaction executed')
            print(out)
            break
        elif reply.lower() in ('n', 'no'):
            print('Transaction cancelled')
            break
        else:
            print('Invalid answer, please input "y" or "n":')

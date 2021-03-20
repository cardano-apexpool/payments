#!/usr/bin/env python3


# Created: 11.03.2021
# Updated: 20.03.2021

import sys
import json
import subprocess
from config import *

env = dict(os.environ)


def get_transactions(address):
    cmd = ["cardano-cli", "query", "utxo", "--address", address, "--" + CARDANO_ERA + "-era", CARDANO_NET, str(MAGIC_NUMBER)]
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    ada_transactions = []
    token_transactions = []
    if not err:
        for line in out.splitlines():
            if 'lovelace' in line:
                transaction = {}
                trans = line.split()
                print('len(trans): %s' % len(trans))
                # if only lovelace
                if len(trans) == 4:
                    transaction['hash'] = trans[0]
                    transaction['id'] = trans[1]
                    transaction['amount'] = trans[2]
                    ada_transactions.append(transaction)
                # if also other tokens
                else:
                    transaction['hash'] = trans[0]
                    transaction['id'] = trans[1]
                    transaction['amounts'] = []
                    tr_amount = {}
                    tr_amount['token'] = trans[3]
                    tr_amount['amount'] = trans[2]
                    transaction['amounts'].append(tr_amount)
                    # for each token
                    for i in range(0, int((len(trans) - 4) / 3)):
                        tr_amount = {}
                        tr_amount['token'] = trans[3 + i * 3 + 3]
                        tr_amount['amount'] = trans[3 + i * 3 + 2]
                        transaction['amounts'].append(tr_amount)
                    token_transactions.append(transaction)
    return ada_transactions, token_transactions, out, err


def create_transaction(src_transactions, src_address, dst_addresses, fee, outfile, validity, amounts=[]):
    incount = 0
    outcount = 0
    amount = 0
    for t in src_transactions:
        amount += int(t['amount'])
    left_amount = amount - fee
    cmd = ["cardano-cli", "transaction", "build-raw"]
    for t in src_transactions:
        tx_in = t['hash'] + '#' + str(t['id'])
        cmd += ["--tx-in", tx_in]
        incount += 1
    """
    if len(dst_addresses) > 1
      - if len(dst_addresses) == len(amounts)
        - if last amount == 0, then send the change to the last address 
        - else then send the change to the source address
      - if len(dst_addresses) == len(amounts) + 1, then send the change to the last address
    if only one dst_address: 
      - if amount == 0, send everything to this address
      - else send the change to the source address 
    """
    # if more than one destination address
    if len(dst_addresses) > 1:
        for i in range(0, len(dst_addresses) - 1):
            cmd.append("--tx-out")
            cmd.append(dst_addresses[i] + '+' + str(amounts[i]))
            left_amount -= amounts[i]
            outcount += 1
        # send the change to the last address
        if (len(dst_addresses) == len(amounts) + 1) or \
          (len(dst_addresses) == len(amounts) and amounts[-1] == 0):
            cmd += ["--tx-out", dst_addresses[i + 1] + '+' + str(left_amount)]
        # send the change to the source address
        else:
            cmd += ["--tx-out", dst_addresses[-1] + '+' + str(amounts[-1])]
            left_amount -= amounts[-1]
            outcount += 1
            cmd += ["--tx-out", src_address + '+' + str(left_amount)]
        outcount += 1
    # if only one destination address
    else:
        # then send the change to source address
        if amounts[0] > 0:
            cmd += ["--tx-out", dst_addresses[0] + '+' + str(amounts[0])]
            left_amount -= amounts[0]
            cmd += ["--tx-out", src_address + '+' + str(left_amount)]
            outcount += 2
        # send everything minus fee to the destination address
        else:
            cmd += ["--tx-out", dst_addresses[0] + '+' + str(left_amount)]
            left_amount = 0
            outcount += 1
    cmd += ["--invalid-hereafter", str(validity), "--fee", str(fee), "--out-file", outfile]
    # debug
    if fee != 200000:
        print(cmd)
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    return out, err, incount, outcount


def calculate_fee(infile, incount, outcount, keys_count):
    cmd = ["cardano-cli", "transaction", "calculate-min-fee", "--tx-body-file", infile, "--tx-in-count", str(incount)]
    cmd += ["--tx-out-count", str(outcount), "--witness-count", str(keys_count), "--byron-witness-count", "0"]
    cmd += ["--testnet-magic", str(MAGIC_NUMBER), "--protocol-params-file", PROTOCOL_FILE]
    # debug
    #print(cmd)
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    return out, err


def sign_transaction(payment_skeys, infile, outfile):
    cmd = ["cardano-cli", "transaction", "sign", "--tx-body-file", infile]
    for pkey in payment_skeys:
        cmd += ["--signing-key-file", pkey]
    cmd += [CARDANO_NET, str(MAGIC_NUMBER), "--out-file", outfile]
    # debug
    print(cmd)
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    return out, err


def submit_transaction(infile):
    cmd = ["cardano-cli", "transaction", "submit", "--tx-file", infile, CARDANO_NET, str(MAGIC_NUMBER)]
    # debug
    print(cmd)
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    return out, err


if __name__ == '__main__':
    # generate the protocol file
    cmd = ["cardano-cli", "query", "protocol-parameters", "--" + CARDANO_ERA + "-era", CARDANO_NET, str(MAGIC_NUMBER), "--out-file", PROTOCOL_FILE]
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        print(err)
        sys.exit(1)
    # query tip
    cmd = ["cardano-cli", "query", "tip", CARDANO_NET, str(MAGIC_NUMBER)]
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        print(err)
        sys.exit(1)
    # set transaction expire time in 300 seconds
    expire = json.loads(out)['slotNo'] + 300

    # get the list of transactions from all source addresses
    src_transactions = []
    src_token_transactions = []
    src_address = ''
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

        trans, token_trans, out, err = get_transactions(src_addr)
        if err:
            print(err)
            sys.exit(1)
        else:
            src_transactions += trans
            src_token_transactions += token_trans
    # debug
    if len(src_transactions) == 0 and len(src_token_transactions) == 0:
        print('No source transactions!')
        sys.exit(1)
    print('Source transactions: %s' % src_transactions)
    print('Source token transactions: %s' % src_token_transactions)
    print('Change address (if required): %s' % src_address)

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
    print('Destination addresses: %s' % dst_addresses)

    # create draft transaction
    out, err, incount, outcount = create_transaction(src_transactions, src_address, dst_addresses, 200000, 'tx.draft', expire, AMOUNTS)
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
    print('Transaction fee: %s' % fee)

    # create transaction
    out, err, incount, outcount = create_transaction(src_transactions, src_address, dst_addresses, fee, 'tx.raw', expire, AMOUNTS)
    if err:
        print(err)
        sys.exit(1)
    print(out)

    # sign transaction
    out, err = sign_transaction(SRC_KEYS, 'tx.raw', 'tx.signed')
    if err:
        print(err)
        sys.exit(1)
    print(out)

    # ask for confirmation before sending the transaction
    while True:
        reply = input('Confirm? [y/n] ')
        if reply.lower() in ('y', 'yes'):
            # submit transaction
            out, err = submit_transaction('tx.signed')
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

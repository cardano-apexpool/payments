import sys
import subprocess
from config import *


def get_transactions(address, tokens_amounts):
    """
    Get the list of transactions from the given addresses.
    :param address: Cardano Blockchain address to search for UTXOs
    :param tokens_amounts: Dictionary where all tokens amounts are saved
    :return: ada_transactions, token_transactions
            ada_transactions: list of transactions with lovelace only
            token_transactions: list of transactions including custom tokens
    """
    cmd = ["cardano-cli", "query", "utxo", "--address", address, "--" + CARDANO_ERA +
           "-era", CARDANO_NET, str(MAGIC_NUMBER)]
    out, err = cardano_cli_cmd(cmd)
    ada_transactions = []
    token_transactions = []
    if not err:
        for line in out.splitlines():
            if 'lovelace' in line:
                transaction = {}
                trans = line.split()
                # if only lovelace
                if len(trans) == 4:
                    transaction['hash'] = trans[0]
                    transaction['id'] = trans[1]
                    transaction['amount'] = trans[2]
                    ada_transactions.append(transaction)
                    # add the lovelace to total amounts to spend
                    if 'lovelace' in tokens_amounts:
                        tokens_amounts['lovelace'] += int(transaction['amount'])
                    else:
                        tokens_amounts['lovelace'] = int(transaction['amount'])
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
                    # add the tokens to total amounts to spend
                    for t in transaction['amounts']:
                        if t['token'] in tokens_amounts:
                            tokens_amounts[t['token']] += int(t['amount'])
                        else:
                            tokens_amounts[t['token']] = int(t['amount'])
    return ada_transactions, token_transactions, out, err


def validate_transaction(spend_amounts, tokens_amounts):
    """
    A transaction is considered valid here if the amounts of tokens
    in the source UTXOs  are greater than or equal to the amounts to spend.
    :param spend_amounts: amounts to spend
    :param tokens_amounts: existing amounts to spend from
    :return: True if transaction is valid, otherwise False
    """
    for am in spend_amounts:
        if am not in tokens_amounts or spend_amounts[am] > tokens_amounts[am]:
            return False
    return True


def create_transaction(src_transactions, src_token_transactions, src_address, dst_addresses,
                       fee, outfile, validity, amounts, l_tokens_amounts):
    """
    Create a transaction file from the given parameters.
    :param src_transactions: UTXOs to consume (only lovelace)
    :param src_token_transactions: UTXOs to consume (lovelace + custom tokens)
    :param src_address: source addresses
    :param dst_addresses: destination addresses
    :param fee: transaction fee
    :param outfile: transaction output file
    :param validity: transaction validity expiration time
    :param amounts: amounts to transfer to each destination address
    :param l_tokens_amounts: amounts of all tokens in the UTXOs (including lovelace)
    :return: incount, outcount: number of UTXOs and number of output transactions, required to calculate the minimum fee
    """
    incount = 0
    outcount = 0
    tokens_amounts = l_tokens_amounts.copy()
    tokens_amounts['lovelace'] -= fee
    cmd = ["cardano-cli", "transaction", "build-raw"]
    for t in src_transactions:
        tx_in = t['hash'] + '#' + str(t['id'])
        cmd += ["--tx-in", tx_in]
        incount += 1
    for t in src_token_transactions:
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
      - if lovelace amount == 0, send everything to this address
      - else send the change to the source address
    """
    # if more than one destination address
    if len(dst_addresses) > 1:
        for i in range(0, len(dst_addresses) - 1):
            cmd.append("--tx-out")
            extra_cmd = dst_addresses[i]
            for ta in amounts[i]:
                extra_cmd += ' + ' + ta['amount'] + ' ' + ta['token']
                tokens_amounts[ta['token']] -= int(ta['amount'])
            cmd += [extra_cmd]
            outcount += 1
        # send the change to the last address
        change = False
        if len(dst_addresses) == len(amounts) + 1:
            cmd += ["--tx-out"]
            extra_cmd = dst_addresses[-1]
            for ta in tokens_amounts:
                if tokens_amounts[ta] > 0:
                    extra_cmd += ' + ' + str(tokens_amounts[ta]) + ' ' + ta
                    tokens_amounts[ta] -= int(tokens_amounts[ta])
        # send the change to the source address
        else:
            cmd += ["--tx-out"]
            extra_cmd = dst_addresses[-1]
            for ta in amounts[i+1]:
                if ta['token'] == 'lovelace' and int(ta['amount']) > 0:
                    extra_cmd += ' + ' + ta['amount'] + ' ' + ta['token']
                    tokens_amounts[ta['token']] -= int(ta['amount'])
                    # change
                    change = True
                else:
                    extra_cmd += ' + ' + str(tokens_amounts[ta['token']]) + ' ' + ta['token']
                    tokens_amounts[ta['token']] -= int(tokens_amounts[ta['token']])
        # check if we have tokens left
        if not change:
            for ta in tokens_amounts:
                if tokens_amounts[ta] > 0:
                    extra_cmd += ' + ' + str(tokens_amounts[ta]) + ' ' + ta
                    tokens_amounts[ta] -= tokens_amounts[ta]
        cmd += [extra_cmd]
        if change:
            cmd += ["--tx-out"]
            extra_cmd = src_address
            for ta in tokens_amounts:
                if tokens_amounts[ta] > 0:
                    extra_cmd += ' + ' + str(tokens_amounts[ta]) + ' ' + ta
                    tokens_amounts[ta] -= int(tokens_amounts[ta])
            cmd += [extra_cmd]
            outcount += 1
        outcount += 1
    # if only one destination address
    else:
        cmd += ["--tx-out"]
        extra_cmd = dst_addresses[0]
        change_to_source = False
        for ta in amounts[0]:
            outcount += 1
            if ta['token'] == 'lovelace' and ta['amount'] == '0':
                # send everything minus fee to the destination address
                extra_cmd += ' + ' + str(tokens_amounts['lovelace']) + ' lovelace'
                tokens_amounts['lovelace'] = 0
            else:
                # send the change to source address
                change_to_source = True
                extra_cmd += ' + ' + ta['amount'] + ' ' + ta['token']
                tokens_amounts[ta['token']] -= int(ta['amount'])
        if not change_to_source:
            # check if we have tokens left
            for ta in tokens_amounts:
                if tokens_amounts[ta] > 0:
                    extra_cmd += ' + ' + str(tokens_amounts[ta]) + ' ' + ta
                    tokens_amounts[ta] -= tokens_amounts[ta]
        cmd += [extra_cmd]

        # if we have change in lovelace
        if tokens_amounts['lovelace'] > 0:
            cmd += ["--tx-out"]
            extra_cmd = src_address
            for ta in tokens_amounts:
                if tokens_amounts[ta] > 0:
                    extra_cmd += ' + ' + str(tokens_amounts[ta]) + ' ' + ta
                    tokens_amounts[ta] -= tokens_amounts[ta]
            cmd += [extra_cmd]
            outcount += 1
    cmd += ["--" + CARDANO_ERA + "-era", "--invalid-hereafter", str(validity), "--fee", str(fee), "--out-file", outfile]
    # debug
    if fee != 200000:
        # print('tokens_amounts left (should be 0 now): %s' % tokens_amounts)
        print('command to execute: %s' % " ".join(cmd))
    out, err = cardano_cli_cmd(cmd)
    return out, err, incount, outcount


def calculate_fee(infile, incount, outcount, keys_count):
    """
    Calculate the minimum transaction fee.
    :param infile: transaction draft file
    :param incount: number of UTXOs
    :param outcount: number ou output transactions
    :param keys_count: number of signing keys
    :return: minimum fee
    """
    cmd = ["cardano-cli", "transaction", "calculate-min-fee", "--tx-body-file", infile, "--tx-in-count", str(incount)]
    cmd += ["--tx-out-count", str(outcount), "--witness-count", str(keys_count), "--byron-witness-count", "0"]
    cmd += ["--testnet-magic", str(MAGIC_NUMBER), "--protocol-params-file", PROTOCOL_FILE]
    out, err = cardano_cli_cmd(cmd)
    return out, err


def sign_transaction(payment_skeys, infile, outfile):
    """
    Sign a raw transaction file.
    :param payment_skeys: payment signing keys
    :param infile: transaction raw file
    :param outfile: transaction signed file
    :return:
    """
    cmd = ["cardano-cli", "transaction", "sign", "--tx-body-file", infile]
    for pkey in payment_skeys:
        cmd += ["--signing-key-file", pkey]
    cmd += [CARDANO_NET, str(MAGIC_NUMBER), "--out-file", outfile]
    out, err = cardano_cli_cmd(cmd)
    return out, err


def transform_amounts(amounts):
    """
    Transform the amounts to be transferred to a dictionary.
    from:
    AMOUNTS = [0]
    to:
    AMOUNTS = [
        [
            {'token': 'lovelace', 'amount': '0'}
        ]
    ]
    :param amounts: amounts to pe transferred
    :return: new_amouts: amounts as a dictionary, total_amounts: dictionary
            with total amounts of each token to be transferred.
    """
    new_amounts = []
    total_amounts = {}
    for am in amounts:
        amount = []
        if isinstance(am, int) or isinstance(am, float):
            if am != 0 and am < 1000000:
                print('Amount too small (%s), it should be at least 1000000 lovelace (1 ADA)!' % am)
                sys.exit(1)
            amount = [{'token': 'lovelace', 'amount': str(am)}]
            if 'lovelace' in total_amounts:
                total_amounts['lovelace'] += am
            else:
                total_amounts['lovelace'] = am
        else:
            for tam in am:
                if isinstance(tam['amount'], int) or isinstance(tam['amount'], float):
                    if tam['amount'] != 0 and tam['amount'] < 1000000:
                        print('Amount too small (%s), it should be at least 1000000 lovelace (1 ADA)!' % tam['amount'])
                        sys.exit(1)
                    tam['amount'] = str(tam['amount'])
                if tam['token'] in total_amounts:
                    total_amounts[tam['token']] += int(tam['amount'])
                else:
                    total_amounts[tam['token']] = int(tam['amount'])
                amount.append(tam)
        new_amounts.append(amount)
    return new_amounts, total_amounts


def cardano_cli_cmd(cmd):
    """
    Execute a cardano-cli command.
    :param cmd: command to execute
    :return: output of the command and error message, if any
    """
    out, err = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        print(err)
        sys.exit(1)
    return out, err

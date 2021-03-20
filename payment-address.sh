#!/bin/bash

KEYS_PATH=keys
ADDRESSES_PATH=addresses
CARDANO_NET="--testnet-magic 1097911063"

#for i in {1..10}
#do
#  cardano-cli address key-gen --verification-key-file ${KEYS_PATH}/payment-${i}.vkey --signing-key-file ${KEYS_PATH}/payment-${i}.skey
#  cardano-cli address build --payment-verification-key-file ${KEYS_PATH}/payment-${i}.vkey --out-file ${ADDRESSES_PATH}/payment-${i}.addr ${CARDANO_NET}
#  echo "$i -> $(cat ${ADDRESSES_PATH}/payment-${i}.addr)"
#done

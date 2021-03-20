#!/bin/bash

KEYS_PATH=keys
ADDRESSES_PATH=addresses
CARDANO_ERA=mary
CARDANO_NET="--testnet-magic 1097911063"

for i in {1..10}
do
  tx=$(cardano-cli query utxo --address $(cat ${ADDRESSES_PATH}/payment-${i}.addr) --${CARDANO_ERA}-era ${CARDANO_NET} | tail -n +3)
  echo "$i -> $(cat ${ADDRESSES_PATH}/payment-${i}.addr) ${tx}"
done

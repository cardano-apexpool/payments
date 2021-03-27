#!/bin/bash

KEYS_PATH=keys
ADDRESSES_PATH=addresses
FILES_PATH=files
CARDANO_NET="--testnet-magic 1097911063"

if [ ! -d ${KEYS_PATH} ] ; then
 mkdir ${KEYS_PATH}
fi

if [ ! -d ${ADDRESSES_PATH} ] ; then
 mkdir ${ADDRESSES_PATH}
fi

if [ ! -d ${FILES_PATH} ] ; then
 mkdir ${FILES_PATH}
fi

for i in {1..10}
do
  if [ -f "${KEYS_PATH}/payment-${i}.skey" ] ; then
    echo "Key already exists!"
  else
    cardano-cli address key-gen --verification-key-file ${KEYS_PATH}/payment-${i}.vkey --signing-key-file ${KEYS_PATH}/payment-${i}.skey
    cardano-cli address build --payment-verification-key-file ${KEYS_PATH}/payment-${i}.vkey --out-file ${ADDRESSES_PATH}/payment-${i}.addr ${CARDANO_NET}
    echo "$i -> $(cat ${ADDRESSES_PATH}/payment-${i}.addr)"
  fi
done

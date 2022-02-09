import os
env = dict(os.environ)

# paths
KEYS_PATH = os.getenv('KEYS_PATH', 'keys')
ADDRESSES_PATH = os.getenv('ADDRESSES_PATH', 'addresses')
FILES_PATH = os.getenv('FILES_PATH', 'files')
LOG_FILE = os.getenv('FILES_PATH', 'files/transactions.log')

# general settings
PROTOCOL_FILE = os.getenv('PROTOCOL_FILE', FILES_PATH + '/protocol-parameters.json')
#CARDANO_NET = os.getenv('CARDANO_NET', '--mainnet')
#MAGIC_NUMBER = os.getenv('MAGIC_NUMBER', '')
CARDANO_NET = os.getenv('CARDANO_NET', '--testnet-magic')
MAGIC_NUMBER = os.getenv('MAGIC_NUMBER', '1097911063')
TRANSACTION_EXPIRE = os.getenv('TRANSACTION_EXPIRE', 300)
MAX_IN_UTXOS = 250

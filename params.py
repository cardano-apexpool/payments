import os
env = dict(os.environ)

# paths
KEYS_PATH = os.getenv('KEYS_PATH', 'keys')
ADDRESSES_PATH = os.getenv('ADDRESSES_PATH', 'addresses')
FILES_PATH = os.getenv('FILES_PATH', 'files')

# general settings
PROTOCOL_FILE = os.getenv('PROTOCOL_FILE', FILES_PATH + '/protocol.json')
CARDANO_ERA = os.getenv('CARDANO_ERA', 'mary')
CARDANO_NET = os.getenv('CARDANO_NET', '--testnet-magic')
MAGIC_NUMBER = os.getenv('MAGIC_NUMBER', '1097911063')
TRANSACTION_EXPIRE = os.getenv('TRANSACTION_EXPIRE', 300)

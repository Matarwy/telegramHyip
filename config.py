_ETH_ADDRESS = '0xd04A0503969182DD97AD61fF61B2Fa288A578DA3'
_DB_NAME = 'ascension.db'
_SUPPORT_ACCOUNT = '@CaptianCrypto'
DEBUG = True


def get_support_account():
    return _SUPPORT_ACCOUNT


def db_name():
    return _DB_NAME


def project_eth_address():
    return _ETH_ADDRESS.lower()

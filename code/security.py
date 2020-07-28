from account import Account

from werkzeug.security import safe_str_cmp


def authenticate(email, password):
    """Use for JWT authentication."""
    account = Account.find_by_email(email=email)
    if account and safe_str_cmp(account.password, password):
        return account


def identity(payload):
    """Use for JWT authentication."""
    account_id = payload["identity"]
    return Account.find_by_id(_id=account_id)

from ..api.account.model import AccountModel

from werkzeug.security import safe_str_cmp


def authenticate(email, password):
    """Use for JWT authentication."""
    account = AccountModel.find_by_email(email=email)
    if account and safe_str_cmp(account.password, password):
        return account


def identity(payload):
    """Use for JWT authentication."""
    account_id = payload["identity"]
    return AccountModel.find_by_id(_id=account_id)

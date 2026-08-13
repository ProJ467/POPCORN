# POPCORN 0.02v
# server/accounts.py

import json
import secrets
import string
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"


def ensure_data_file():
    """Create the data directory and accounts file if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not ACCOUNTS_FILE.exists():
        ACCOUNTS_FILE.write_text("{}", encoding="utf-8")


def load_accounts():
    """Load all accounts from accounts.json."""
    ensure_data_file()

    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, OSError):
        return {}


def save_accounts(accounts):
    """Save all accounts to accounts.json."""
    ensure_data_file()

    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            accounts,
            file,
            indent=4,
            ensure_ascii=False
        )


def generate_account_id(length=12):
    """Generate a random Account ID."""

    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def account_id_exists(account_id, accounts=None):
    """Check whether an Account ID already exists."""

    if accounts is None:
        accounts = load_accounts()

    return account_id in accounts


def create_account():
    """Create and save a new account."""

    accounts = load_accounts()

    # Generate an ID that does not already exist
    while True:
        account_id = generate_account_id()

        if not account_id_exists(account_id, accounts):
            break

    account = {
        "id": account_id,
        "projects": []
    }

    accounts[account_id] = account

    save_accounts(accounts)

    return account


def get_account(account_id):
    """Get an account by Account ID."""

    accounts = load_accounts()

    return accounts.get(account_id)


def account_exists(account_id):
    """Return True if an account exists."""

    accounts = load_accounts()

    return account_id in accounts


def delete_account(account_id):
    """Delete an account."""

    accounts = load_accounts()

    if account_id not in accounts:
        return False

    del accounts[account_id]

    save_accounts(accounts)

    return True
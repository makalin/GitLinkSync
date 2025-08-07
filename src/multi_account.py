import json
import random
from typing import List, Dict

class AccountManager:
    def __init__(self, config_file='accounts.json'):
        self.config_file = config_file
        self.accounts = self.load_accounts()
        self.current_github_index = 0
        self.current_x_index = 0

    def load_accounts(self) -> Dict:
        """Load accounts from configuration file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'github': [],
                'x': []
            }

    def save_accounts(self):
        """Save accounts to configuration file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.accounts, f, indent=2)

    def add_github_account(self, token: str, username: str = None):
        """Add a GitHub account."""
        account = {'token': token, 'username': username}
        self.accounts['github'].append(account)
        self.save_accounts()

    def add_x_account(self, username: str, password: str):
        """Add an X account."""
        account = {'username': username, 'password': password}
        self.accounts['x'].append(account)
        self.save_accounts()

    def get_next_github_account(self) -> Dict:
        """Get next GitHub account in rotation."""
        if not self.accounts['github']:
            raise Exception("No GitHub accounts configured")
        
        account = self.accounts['github'][self.current_github_index]
        self.current_github_index = (self.current_github_index + 1) % len(self.accounts['github'])
        return account

    def get_next_x_account(self) -> Dict:
        """Get next X account in rotation."""
        if not self.accounts['x']:
            raise Exception("No X accounts configured")
        
        account = self.accounts['x'][self.current_x_index]
        self.current_x_index = (self.current_x_index + 1) % len(self.accounts['x'])
        return account

    def get_random_github_account(self) -> Dict:
        """Get a random GitHub account."""
        if not self.accounts['github']:
            raise Exception("No GitHub accounts configured")
        return random.choice(self.accounts['github'])

    def get_random_x_account(self) -> Dict:
        """Get a random X account."""
        if not self.accounts['x']:
            raise Exception("No X accounts configured")
        return random.choice(self.accounts['x'])

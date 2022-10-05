#Parent Class
class Account: 
    def __init__(self, name, account_number, balance, account_type):
        self.name = name
        self.account_number=account_number
        self.balance=balance
        self.account_type=account_type

# Child classes of Account
class Checking(Account):
    def __init__(self, name, account_number, balance):
        self.account_type = "Checking"


class Savings(Account):
    def __init__(self, name, account_number, balance):
        self.account_type = "Savings"

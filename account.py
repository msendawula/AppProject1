class Account: 
    isOpen = True

    def __init__(self, name, account_number, balance, account_type):
        self.name = name
        self.account_number=account_number
        self.balance=balance
        self.account_type=account_type

    def __str__(self):
        return self.name + "," + str(self.account_number) +"," +(self.balance) +"," + str(self.account_type)

# Child class of Account

   
class Checking(Account):
    def __init__(self, name, account_number, balance):
        self.name = name
        self.account_number=account_number
        self.balance=balance
        self.account_type = "Checking"

class Savings(Account):
    def __init__(self, name, account_number, balance):
        self.name = name
        self.account_number=account_number
        self.balance=balance
        self.account_type = "Savings"


def main():
    a1 = Checking("James Jones", 55855864, 550.65, Checking)
    c1 = Savings("George Lam", 55856658566, 90005.65, Savings)
    d1 = Savings("Jesse Lane", 85545755, 905.25, Savings)
    print(a1)

if __name__ == '__main__':
    main()

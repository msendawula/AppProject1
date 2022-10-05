from pymongo import MongoClient


def main():
    client = MongoClient()

    BankAccountsdb = client.BankAccounts
    
    print("Welcome to the QuickTeller Application".center(75,"="))

    while True:
        print("Please select an option:")
        print("\ta) Add New Account")
        print("\tb) View Account")
        print("\tc) Update Account")
        print("\td) Close Account")
        print("\tq) Quit")
        option = input(">>>")

        if option == "q":
            break

        if option == "a":
#Setting account type
            print("What type of account does the customer want to open?")
            print("\t a) Opening a Checking Account")
            print("\t b) Opening a Savings Account")
            if input(">>>").lower() == "a":
                print("You've chosen a Checking Account.")
                type = "Checking"
            else:
                print("You've chosen a Savings Account.")
                type = "Savings"

#Setting Account Holder Name               
            print("\n\nEnter Account Holder name (First Name | Last Name):")
            name = input(">>>")

#Setting Account Number
            import random
            print("\n\nAssigning random account number.")
            account_number = random.randint(25,600)

#Setting up Starting Balance
            print("\n\n Enter Starting Balance:")
            balance=float(input(">>>"))
            newAccountDict = {"Name": name, "Account Number": account_number, "Balance": balance, "Account Type":type}
            BankAccountsdb.accounts.insert_one(newAccountDict)
            print(f"The following account information has been inserted into the Database:{newAccountDict}.")

#Allowing for database to be queried by Customer Name or Account Number
        if option == "b":
            print("Please enter Account Holder name or Account Number")
            print("\ta) Account Number")
            print("\tb) Account Holder Name")
            AccountOption = input(">>>")
        
            if AccountOption == "a":
                print("\t Please enter the Account Number")
                option = int(input(">>>"))
                x  = BankAccountsdb.accounts.find_one({"Account Number": option},{"_id":0})
                print(x)
                            

            if AccountOption == "b":
                print("\t Please enter the Account Holder Name")
                option = input(">>>")              
                x = BankAccountsdb.accounts.find_one({"Name": option},{"_id":0})
                print(x)

#Code to allow for deposits/withdrawals
        if option == "c":
            print("\tWhat action would you like to perform?")
            print("\ta) Deposit Funds")
            print("\tb) Withdraw Funds")
            BankTransact = input(">>>")


            if BankTransact == "a":
                print("\tPlease enter the Account Number")
                option = int(input(">>>"))
                print("Please enter the deposit amount.")
                option1 = float(input(">>>"))
#Teller may enter a positive or negative number; Want to make sure that regardless of whether a negative or positive number is entered number entered is added to balance. 
                Deposit = float(abs(option1))
                BankAccountsdb.accounts.update_one({"Account Number": option}, {"$inc": {"Balance":Deposit}})
                


            if BankTransact == "b":
                print("\tPlease enter the Account Number")
                option = int(input(">>>"))
                print("Please enter the withdrawal amount.")
                option1 = float(input(">>>"))
#Teller may enter a positive or negative number; Want to make sure that regardless of whether a negative or positive number is entered number entered is deducted from balance. 
                Withdrawal = -1*(abs(option1))
                BankAccountsdb.accounts.update_one({"Account Number": option}, {"$inc": {"Balance":Withdrawal}})
                  

#Code to delete account from database
        if option == "d":
            print("Please enter the Account Number you wish to close.")
            option = int(input(">>>"))
            BankAccountsdb.accounts.delete_one({"Account Number": option})
           


if __name__ == "__main__":
    main()

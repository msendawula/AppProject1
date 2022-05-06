import account
import csv
from pymongo import MongoClient

def add_account() -> account.Account:
    print("Welcome to QuickTeller. Please select an action:")
    print("\t a) Opening a Savings Account")
    print("\t b) Opening a Checking Account")
    typeAccount = input(">>>")

    if not typeAccount == 'a':
        typeAccount ='b'
        print("Default Checking Option chosen.")

    print("\n\nEnter Account Holder name (First Name | Last Name):")
    name = input(">>>")

    print("\n\n Enter new Account Number:")
    account_number = int(input(">>>"))

    print("\n\n Enter Starting Balance:")
    balance=str(float(input(">>>")))

    if typeAccount == "a":
        newAccount = account.Savings(name, account_number, balance)
    else:
        newAccount = account.Checking(name, account_number, balance)
    return newAccount



def load_accounts():
    f = open("saved_accounts.txt", "r")
    lst_accounts = []
    for line in f:
        if line ==" ":
            break
        account_data = line.split(',')
        if account_data [3] == "Savings":
            newAccount = account.Savings(account_data[0], account_data[1], account_data[2])
        else: 
            newAccount = account.Checking(account_data[0], account_data[1], account_data[2])
        lst_accounts.append(newAccount)
    f.close()
    return lst_accounts


def save_accounts (lst_Accounts):
    f = open("saved_accounts.txt", "w")
    for account in lst_Accounts:
        f.write(account.name + ","+ str(account.account_number) + ","+str(account.balance) +"," + account.account_type + "\n")
    f.close()
    import pandas
    bankaccounts=pandas.read_csv("saved_accounts.txt", header = [0])
    bankaccounts.to_csv("saved_bankaccounts.csv", index = None)
                

def main():
    client = MongoClient()

    BankAccountsdb = client.BankAccounts

    print("Welcome to the QuickTeller Application")
    
    lst_Accounts = load_accounts()

    while True:
        print("Please select an option:")
        print("\ta) Add New Account")
        print("\tb) View Account")
        print("\tc) Update Account")
        print("\td) Close Account")
        print("\ts) Save all accounts to MongoDB (Must restart application before saving.)")
        print("\tq) Quit")
        option = input(">>>")

        if option == "q":
            break

        elif option == "s":
            client.drop_database("BankAccounts")
            for bkacct in lst_Accounts:
                save_to_db(bkacct, BankAccountsdb)

        if option == "a":
            lst_Accounts.append(add_account())
            save_accounts(lst_Accounts)     

        if option == "b":
            print("Please enter Account Holder name or Account Number")
            print("\ta) Account Number")
            print("\tb) Account Holder Name")
            AccountOption = input(">>>")
        
            if AccountOption == "a":
                print("\t Please enter the Account Number")
                option = input(">>>")
                with open("saved_bankaccounts.csv") as c:
                    reader = csv.reader(c)
                    for row in reader:
                        if row[1]==option:
                            print(row)
                            

            if AccountOption == "b":
                print("\t Please enter the Account Holder Name")
                option = input(">>>")                
                with open("saved_bankaccounts.csv") as c:
                    reader = csv.reader(c)
                    for row in reader:
                        if row[0]==option:
                            print(row)  

        if option == "c":
            print("\tWhat action would you like to perform?")
            print("\ta) Deposit Funds")
            print("\tb) Withdraw Funds")
            BankTransact = input(">>>")
        

            if BankTransact == "a":
                import decimal
                print("\tPlease enter the Account Number")
                option = input(">>>")
                print("Please enter the deposit amount.")
                Deposit = input(">>>")
                updated_row=[]
                with open("saved_bankaccounts.csv","r") as d:
                    csvreader = csv.reader(d)
                    for row in csvreader:
                            if option == row[1]:
                                row[2] = ((float(row[2])) + (float(Deposit)))
                                updated_row.append(row)
                            else:
                                updated_row.append(row)
                    with open("saved_bankaccounts.csv", "w", newline="") as e:
                        writer=csv.writer(e)
                        writer.writerows(updated_row)
                    import pandas
                    df=pandas.read_csv("saved_bankaccounts.csv", header = [0])
                    df.to_csv("saved_accounts.txt", header=False, index = None)


            if BankTransact == "b":
                import decimal
                print("\tPlease enter the Account Number")
                option = input(">>>")
                print("Please enter the withdrawal amount.")
                Withdrawal = input(">>>")
                updated_row=[]
                with open("saved_bankaccounts.csv","r") as d:
                    csvreader = csv.reader(d)
                    for row in csvreader:
                            if option == row[1]:
                                row[2] = ((float(row[2])) - (float(Withdrawal)))
                                updated_row.append(row)
                            else:
                                updated_row.append(row)
                    with open("saved_bankaccounts.csv", "w", newline="") as e:
                        writer=csv.writer(e)
                        writer.writerows(updated_row)
                    import pandas
                    df=pandas.read_csv("saved_bankaccounts.csv", header = [0])
                    df.to_csv("saved_accounts.txt", header=False, index = None)     


        if option == "d":
            print("Please enter the Account Number you wish to delete")
            option = input(">>>")
            lines=[]
            try:
                with open("saved_accounts.txt", "r") as rf:
                    lines = rf.readlines()
                with open("saved_accounts1.txt", "w") as rg:
                    for line in lines:
                        if option not in line:
                            rg.write(line)
            except:
                print("Error found. Please try again.")

            with open ("saved_accounts1.txt", "r") as source, open("saved_accounts.txt", "w") as destination:
                for line in source:
                    destination.write(line)
            import pandas
            bankaccounts=pandas.read_csv("saved_accounts.txt", header = [0])
            bankaccounts.to_csv("saved_bankaccounts.csv", index = None)


def save_to_db(bkacct, BankAccountsdb):
    dict_acct = {"name": bkacct.name, "account_number": bkacct.account_number, "balance": bkacct.balance, "account_type": bkacct.account_type}
    BankAccountsdb.accounts.insert_one(dict_acct)



if __name__ == "__main__":
    main()

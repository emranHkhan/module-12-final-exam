from datetime import datetime

class Bank:
    def __init__(self, name, bank_balance):
        self.name = name
        self.user = []
        self.loan_taken = 0
        self.loan_amount = 0
        self.can_give_loan = True
        self.bank_balance = bank_balance
        self.is_bankrupt = False
    
class Admin:
    def __init__(self, bank):
        self.bank = bank
        self.admin = [{'name': 'super_admin', 'password' : 'admin1234'}]
        self.is_logged_in = False

    def login(self, password):
        for admin in self.admin:
            for name, admin_password in admin.items():
                if password == admin_password:
                    self.is_logged_in = True
                    self.bank.admin = {'name': name, 'admin_password': password}
                    print("Login successful!\n")
                    return 
                
        print("Incorrect password. Access denied.\n")

    def logout(self):
        self.is_logged_in = False
        self.bank.admin = None
        print("Logged out.\n")

    def make_bank_bankrupt(self):
        self.bank.is_bankrupt = True
        self.bank.bank_balance = 0
        return True
    
    def create_admin(self, name, password):
        self.admin.append({'name': name, 'password': password})
    
    def check_bank_balance(self):
        print("Total balance of the bank is " + str(self.bank.bank_balance) + "\n")

    def check_loan_amount(self):
        print(f"Total loan amount is {self.bank.loan_amount}\n")
        
    def show_users(self):
        print("\tAccount_No\t\tName\tEmail\t\tAddress\t\tBalance\n")
        for item in self.bank.user:
            for account_no, details in item.items():
                print(f"\t{account_no}\t{details['name']}\t{details['email']}\t{details['address']}\t{details['balance']}\n")
    
    def delete_user(self, account_no):
        new_users_list = []

        for account in self.bank.user:
            if account_no not in account:
                new_users_list.append(account)

        self.bank.user = new_users_list
        print("User deleted successfully.\n")
    
    def toggle_loan_feature(self):
        self.bank.can_give_loan = not self.bank.can_give_loan

        if self.bank.can_give_loan:
            print("loan feature enabled.\n")
        else:
            print("loan feature disabled.\n")
        

class User:
    def __init__(self, bank):
        self.bank = bank
        self.transaction_history = []
        self.is_logged_in = False
        self.name = None
        self.email = None
        self.password = None
        self.address = None
        self.account_type = None
        self.user_account_no = None

    def register(self, name, email, password, address, account_type):
        user_account_no = name + email
        self.bank.user.append({user_account_no: {'name': name, 'email': email, 'password': password,'address': address, 'account_type': account_type, 'balance': 0}})

        self.user_account_no = user_account_no
        self.name = name
        self.account_type = account_type
        self.email = email
        self.password = password
        self.address = address

    def login(self, email, password):
        for user_data in self.bank.user:
            for user_account_no, user_info in user_data.items():
                if user_info['email'] == email and user_info['password'] == password:
                    self.is_logged_in = True
                    self.user_account_no = user_account_no
                    print("Login successful!\n")
                    return
        print("Incorrect email or password. Access denied.\n")



    def logout(self):
        self.is_logged_in = False
        self.bank.user = []
        print("Logged out.\n")
    
    def deposit(self, amount):
        for account in self.bank.user:
            if self.user_account_no in account:
                account[self.user_account_no]['balance'] += amount
                self.bank.bank_balance += amount
                self.transaction_history.append({'amount': amount, 'time': datetime.now(), 'method': 'deposit'})
                print (f"{amount}/= is deposited to your account.\n")
                return

    def withdraw(self, amount):
        if self.bank.is_bankrupt:
            print("Sorry, the bank is broken! Your money is successfully laundered to the Swiss bank\n")
            return

        for account in self.bank.user:
           if self.user_account_no in account:
                if account[self.user_account_no]['balance'] < amount:
                    print("Withdrawal amount exceeded.\n")
                    break

                account[self.user_account_no]['balance'] -= amount
                self.bank.bank_balance -= amount
                self.transaction_history.append({'amount': amount, 'time': datetime.now(), 'method': 'withdraw'})
                print (f"{amount}/= is withdrawn from your account.\n")
                break

    def get_balance(self):
        for account in self.bank.user:
            if self.user_account_no in account:
                print(f"Your current balance is {account[self.user_account_no]['balance']}/=.\n")
                return
               
    
    def get_transaction_history(self):
        print("Amount\t\t\tTime")
        for history in self.transaction_history:
            if history['method'] == 'deposit':
                print(f"Deposit: {history['amount']}/=\t\t{history['time']}\n")
            else:
                print(f"Withdraw: {history['amount']}/=\t\t{history['time']}\n")
    
    def get_loan(self, amount):
        if self.bank.loan_taken == 2:
            print("Sorry, you have already taken maximum number of loan\n")
            return
        
        if amount > self.bank.bank_balance or not self.bank.can_give_loan:
            print("Sorry, the amount cannot be granted.\n")
            return
        
        if self.bank.is_bankrupt:
            print("Sorry, the bank is broken! Your money is successfully laundered to the Swiss bank\n")
            return
        
        print(f"{amount}/= loan granted.\n")
        self.bank.loan_taken += 1
        self.bank.bank_balance -= amount
        self.bank.loan_amount += amount
        self.deposit(amount)


    def transfer_money(self, amount, recipient_account_no):
        recipient_found = False
        for account in self.bank.user:
            for user_account_no, user_info in account.items():
                if user_account_no == recipient_account_no:
                    recipient_found = True
                    user_info['balance'] += amount
                    break

        if recipient_found:
            print(f"{amount} transferred to {recipient_account_no}\n")
            for index, account in enumerate(self.bank.user):
                for user_account_no, user_info in account.items():
                    if user_account_no == self.user_account_no:
                        current_user = self.bank.user[index]
                        current_user[user_account_no]['balance'] -= amount
                        self.bank.user[index] = current_user
                        return

        if not recipient_found:
            print("Recipient account not found.\n")



bank = Bank('Basic', 10000)
admin = Admin(bank)

while True:
    print('Type 1 to continue as a user: \n')
    print('Type 2 to continue as an admin: ')
    choice1 = int(input("\nType: "))


    if choice1 == 1:
        print('\nType 1 for registration')
        print('\nType 2 for login')

        auth = int(input("\nType: "))

        user = User(bank)

        if auth == 1:
            name=input("\nName: ")
            email=input("Email: ")
            password=input("Password: ")
            address=input("Address: ")
            account_type=input("Account Type: ")

            user.register(name, email, password, address, account_type)
            user.is_logged_in = True
            is_user_logged_in = True
            print("Bank's user list after registration:", user.bank.user)

        elif auth == 2:
            email=input("Email: ")
            password=input("Password: ")
            user.login(email, password)

            if not user.is_logged_in:
                continue
        
        else:
            continue

        while True:
            print("\nType 1 to deposit")
            print("Type 2 to withdraw")
            print("Type 3 for loan")
            print("Type 4 to check balance")
            print("Type 5 to see transaction history")
            print("Type 6 to Transfer money")
            print("Type 7 to log out")

            choice2 = int(input("\nType: "))

            if not user.is_logged_in:
                print("Please login to your account.")
                continue

            if choice2 == 1:
                amount = int(input("\nEnter deposit amount: "))
                user.deposit(amount)
            
            elif choice2 == 2:
                amount = int(input("\nEnter withdraw amount: "))
                user.withdraw(amount)
            
            elif choice2 == 3:
                amount = int(input("\nEnter loan amount: "))
                user.get_loan(amount)

            elif choice2 == 4:
                user.get_balance()

            elif choice2 == 5:
                user.get_transaction_history()

            elif choice2 == 6:
                amount = int(input("\nEnter amount: "))
                recipient_account_no = input("Enter recipient account number: ")
                user.transfer_money(amount, recipient_account_no)
            elif choice2 == 7:
                user.logout()
                is_user_logged_in = False
                break
            else:
                continue

    elif choice1 == 2:
        admin_password = input("\nEnter admin password: ")    
        admin.login(admin_password)

        if not admin.is_logged_in:
          continue  


        while True:
            if not admin.is_logged_in:
                break

            print("\nType 1 for creating admin")
            print("Type 2 to check balance")
            print("Type 3 to see check loan amount")
            print("Type 4 to show all the users")
            print("Type 5 to delete a user")
            print("Type 6 to toggle the loan feature")
            print("Type 7 to log out the admin")

            choice3 = int(input("\nType: "))

            if choice3 == 1:
                name = input("\nEnter name: ")
                password = input("Enter password: ")

                admin.create_admin(name, password)

            elif choice3 == 2:
                admin.check_bank_balance()
            elif choice3 == 3:
                admin.check_loan_amount()
            elif choice3 == 4:
                admin.show_users()
            elif choice3 == 5:
                user_account_no = input("\nEnter user account no: ")
                admin.delete_user(user_account_no)
            elif choice3 == 6:
                admin.toggle_loan_feature()
            elif choice3 == 7:
                admin.logout()
            else:
                continue
    else:
        continue

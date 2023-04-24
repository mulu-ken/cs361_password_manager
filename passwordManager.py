import getpass
import sys
import os

import stdiomask
import smtplib
from clint.textui import puts, colored, prompt
from termcolor import colored

password_data = {
    "mulukenme2023@gmail.com": {
        "user_name": "mukluk",
        "master_password": "12345",
        "accounts": {
            "facebook": {"username": "mulukeaddn@gmail.com",
                         "password": "112345"},
            "google": {"username": "muluken@gmail.com",
                       "password": "7890123"}
        }

    },

    "mulukenme2024@gmail.com": {
        "user_name": "muklukeeen",
        "master_password": "fhkjdkhjdkhj",
        "accounts": {
            "facebook": {"username": "dhhdjd@gmail.com",
                         "password": "17denhcjc"},
            "google": {"username": "muluken@hostpace.com",
                       "password": "1ghdvsjhiozhkjdfn"}
        }

    },

}


def forgot_password():
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - PASSWORD RECOVERY", 'green', attrs=['bold']))
    print("########################################################################################")
    global password_data
    print("Your choice: 3")
    print("--Forgot password--")
    email = input('Please enter your email:\n>>')

    print(f"email is {email}")

    dict_printer(password_data)

    # Check if email exists in password_data
    if email in password_data:
        # Generate a temporary password and update the password_data
        import random
        import string
        temp_password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        password_data[email]['master_password'] = temp_password

        # Send the temporary password to the user's email
        from_email = 'mamom@oregonstate.edu'
        from_password = temp_password
        to_email = email
        subject = 'Password Reset'
        body = f'Your temporary password is {temp_password}. Please use this password to login and reset your password.'
        message = f'Subject: {subject}\n\n{body}'
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(from_email, from_password)
            smtp.sendmail(from_email, to_email, message)

        print('A temporary password has been sent to your email. Please login with this password to reset your '
              'password.')
    else:
        print('Email not found. Please try again.')


def welcome():
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - WELCOME", 'green', attrs=['bold']))
    print("########################################################################################")
    print("Thank you for using Password Manager to keep your accounts secure!")
    print("")
    print(colored("Please select an option:", 'black', attrs=['bold']))
    print(colored("1. Login to an existing account", 'green'))
    print(colored("2. Register for a new account", 'green'))
    print(colored("3. Forgot password", 'green'))
    print(colored("4. Exit", 'red'))
    print("")
    option = input(colored(">> ", 'green'))

    if option == '1':
        _ = os.system('cls')
        # Move the cursor to the top of the terminal
        login(password_data)
        # # If not, show error message and return to main menu
        # print('Logging in...')
        # print('You have successfully logged in to your account! Press enter to continue...')
        # input()
    elif option == '2':
        # Show registration form and register a new account
        # After successful registration, show dashboard
        _ = os.system('cls')
        register()
    elif option == '3':
        # Show forgot password form and send reset link to email
        # After successful reset, show login form
        _ = os.system('cls')
        forgot_password()
    elif option == '4':
        _ = os.system('cls')
        print(colored('Goodbye!', 'green', attrs=['bold']))
        exit()
    else:
        _ = os.system('cls')
        print(colored('Invalid option. Please try again.', 'red', attrs=['bold']))


def login(password_dict):
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - LOGIN", 'green', attrs=['bold']))
    print("########################################################################################")

    print("Your choice: 1 or login")
    print("---Login into your account---")
    email = input('Please enter your email address:\n>> ')
    password = input('Please enter your master password:\n>> ')

    # Check if email and password are valid and match with an existing account
    # If yes, then log in and show dashboard
    if email in password_dict and \
            password_dict[email]["master_password"] == password:
        name = password_dict[email]["user_name"]
        print('Logging in...')
        print('You have successfully logged in to your account! Press enter to continue...')
        input()
        _ = os.system('cls')
        show_dashboard(name, email, password)

    else:
        _ = os.system('cls')
        # show error message and return to the main menu
        print('Invalid email or password. Please try again or register for a new account')
        welcome()


def password_store(email):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - STORE PASSWORD", 'green', attrs=['bold']))
    print("########################################################################################")

    global password_data
    print("")
    print("Your choice: N for storing password for a new account")

    # check if the password is strong enough
    while True:
        print("Enter the account name")
        account_name = input(">>")
        print("Enter the username for the account: ")
        username = input(">>")
        strong_pass = getpass.getpass("Enter a strong password for the account:\n> ")

        # check the strength of the password
        while True:
            if len(strong_pass) < 8:
                print("The password should be atleast 8 characters long")
            elif not any(char.isdigit() for char in strong_pass):
                print("The password should contain at least one digit")
            elif not any(char.isupper() for char in strong_pass):
                print("The password should contain at least one upper case letter")
            elif not any(char.lower() for char in strong_pass):
                print("The password should contain at least one lower case letter")
            elif not any(char in "!@#$%^&*()_+-=[]{};:'\"\\|,.<>?/" for char in strong_pass):
                print("The password should contain at least one special character")
            else:
                break

            strong_pass = getpass.getpass("Enter a strong password for the account:\n> ")

        # store the password for the account in the dictionary
        password_data[email]["accounts"][account_name] = {username: strong_pass}

        print("Password stored successfully!")

        # Ask the user if they want to store another password or go back to the main menu
        while True:
            response = input(
                "To view your stored passwords, type 'view'. To store another password, type 'store'. To go back to "
                "the main menu, type 'menu'.\n> ")
            if response.lower() == "view":
                name = password_data[email]["user_name"]
                password = password_data[email]["master_password"]
                _ = os.system('cls')
                show_dashboard(name, email, password)
            elif response.lower() == "store":
                break
            elif response.lower() == "menu":
                print("\nReturning to main menu...\n")
                welcome()
            else:
                print("\nInvalid input. Please try again.\n")


def account_delete(email):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - DELETE AN ACCOUNT", 'green', attrs=['bold']))
    print("########################################################################################")

    print("Enter '1' to confirm account deletion ")
    print("Enter 2 to cancel")

    while True:
        confirmation = input(colored(">", 'red', attrs=['bold']))

        if confirmation == "1":
            print(colored("WARNING: This action can not be undone! Enter your master password"
                          " to confirm account deletion", 'red', attrs=["bold"]))
            pass_input = input(">")
            if pass_input == password_data[email]["master_password"]:
                del password_data[email]
                print(
                    f"Account successfully deleted. We are sorry to see you go. Press enter to exit")
                input()
                welcome()
                break
            else:
                print("Please enter the correct master password for the account")

        elif confirmation == "2":
            name = password_data[email]["user_name"]
            password = password_data[email]["master_password"]
            show_dashboard(name, email, password)
            break


def account_management(email):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - ACCOUNT MANAGEMENT", 'green', attrs=['bold']))
    print("########################################################################################")

    global password_data

    while True:
        print("Enter '1' to change your master password")
        print("Enter '2' to delete your account")

        user_data = input(">")

        if user_data == '1':
            # check the strength of the password
            while True:
                strong_pass = getpass.getpass("Enter a strong password for the master account:\n> ")
                if len(strong_pass) < 8:
                    print("The password should be atleast 8 characters long")
                elif not any(char.isdigit() for char in strong_pass):
                    print("The password should contain at least one digit")
                elif not any(char.isupper() for char in strong_pass):
                    print("The password should contain at least one upper case letter")
                elif not any(char.lower() for char in strong_pass):
                    print("The password should contain at least one lower case letter")
                elif not any(char in "!@#$%^&*()_+-=[]{};:'\"\\|,.<>?/" for char in strong_pass):
                    print("The password should contain at least one special character")
                else:
                    break

            password_data[email]["master_password"] = strong_pass
            print("You have successfully updated the password for the master account. Press enter to continue...")
            input()

            user_name = password_data[email]["user_name"]

            show_dashboard(user_name, email, strong_pass)
            break

        elif user_data == '2':
            account_delete(email)
            break


def logout(email):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - LOGOUT", 'green', attrs=['bold']))
    print("########################################################################################")
    print("")

    print("Are you sure you want to logout?y/n\n")
    print("Press 'y' to confirm logout, or 'n' to return to the dashboard: ")
    confirmation = input(">")

    if confirmation.lower() == 'y':
        print("You have been successfully logged out. Returning to the main menu")
        welcome()
    else:

        user_name = password_data[email]["user_name"]
        password = password_data[email]["master_password"]
        print("Returning to the main menu. Please enter to continue")
        input()
        show_dashboard(user_name, email, password)


def update_password(email):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - UPDATE PASSWORD FOR AN ENTRY", 'green', attrs=['bold']))
    print("########################################################################################")
    print("")
    global password_data
    print(colored("Here are your account details:", 'blue', attrs=['bold']))
    dict_printer(password_data[email]["accounts"])

    while True:
        account_name = input("Please enter the account name you want to update password for:\n> ")

        for acc_name, acc_data in password_data[email]["accounts"].items():
            if acc_name == account_name:
                user_name = acc_data["username"]
                curren_pass = acc_data["password"]

                print("The username name is: ", user_name)
                print("Your current password is", curren_pass)

            else:
                break

        while True:
            strong_pass = getpass.getpass("Enter a strong password for the account above:\n> ")
            # check the strength of the password

            if len(strong_pass) < 8:
                print("The password shuld be at least 8 characters long")
            elif not any(char.isdigit() for char in strong_pass):
                print("The password should contain at least one digit")
            elif not any(char.isupper() for char in strong_pass):
                print("The password should contain at least one upper case letter")
            elif not any(char.lower() for char in strong_pass):
                print("The password should contain at least one lower case letter")
            elif not any(char in "!@#$%^&*()_+-=[]{};:'\"\\|,.<>?/" for char in strong_pass):
                print("The password should contain at least one special character")
            else:
                break

        password_data[email]["accounts"][account_name]["password"] = strong_pass

        print(f"You have successfully updated your password for {account_name} account! Press enter to continue...")
        input()

        name = password_data[email]["user_name"]
        password = password_data[email]["master_password"]
        show_dashboard(name, email, password)
        break


def delete_password_entry(email):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - DELETE PASSWORD ENTRY", 'green', attrs=['bold']))
    print("########################################################################################")
    print("")
    global password_data
    print(colored("Here are your account details:", 'blue', attrs=['bold']))
    dict_printer(password_data[email]["accounts"])

    while True:
        print(colored("Please enter the account name that you would like to delete", 'red', attrs=['bold']))
        account_name = input(">")

        if account_name in password_data[email]["accounts"]:
            print(f"Are you sure you would like to delete the password entry for {account_name}? y/n")
            confirmation = input(colored(">", 'red', attrs=['bold']))

            if confirmation.lower() == "y":
                del password_data[email]["accounts"][account_name]
                print(
                    f"You have successfully deleted your password for {account_name} account! Press enter to continue...")
                input()
                break  # exit the while loop if account is deleted

        else:
            print("The account information does not exist. Please enter a valid account name.")

    user_name = password_data[email]["user_name"]
    password = password_data[email]["master_password"]
    show_dashboard(user_name, email, password)


def password_generate():
    pass


def password_meter(email):
    pass


def help_menu(email):
    global password_data
    _ = os.system('cls')

    print("########################################################################################")
    print(colored("PASSWORD MANAGER - HELP MENU", 'green', attrs=['bold']))
    print("########################################################################################")

    print("")
    print('List of Help Commands')
    print("- login: login to an existing account")
    print("- register: register for a new account")
    print("- dashboard: view stored accounts and passwords")
    print("- store: store a new password")
    print("- retrieve: retrieve a stored password")
    print("- generate: generate a new password")
    print("- strength: check password strength")
    print("- manage: manage account details")
    print("- delete: delete an account")
    print("- help: display this help menu")
    print("- exit: exit the program")

    user_name = password_data[email]["user_name"]
    password = password_data[email]["master_password"]

    while True:
        choice = input("> ")

        if choice.lower() == 'login':
            login(password_data)
            break

        elif choice.lower() == 'register':
            register()
            break

        elif choice.lower() == 'dashboard':
            show_dashboard(user_name, email, password)
            break

        elif choice.lower() == 'store':
            password_store(email)
            break

        elif choice.lower() == 'generate':
            password_generate(email)
            break

        elif choice.lower() == 'strength':
            password_meter(email)
            break

        elif choice.lower() == 'manage':
            account_management(email)
            break

        elif choice.lower() == 'delete':
            account_delete(email)
            break

        elif choice.lower() == 'help':
            help_menu(email)

        elif choice.lower() == 'exit':
            sys.exit()



def password_retrieve(email, choice):
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - PASSWORD RETRIEVAL", 'green', attrs=['bold']))
    print("########################################################################################")

    stored_accounts = {}
    num = 0
    for account in password_data[email]["accounts"].keys():
        num += 1
        stored_accounts[num] = account

    this_account = stored_accounts[int(choice)]
    password = password_data[email]["accounts"][this_account]["password"]
    user_name = password_data[email]["accounts"][this_account]["username"]

    print(f"username: {user_name}")
    print(f"password: {password}")
    input("\nPress enter to continue...")
    user_name = password_data[email]["user_name"]
    password = password_data[email]["master_password"]
    show_dashboard(user_name, email, password)


def show_dashboard(name, email, password):
    _ = os.system('cls')
    global password_data
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - DASHBOARD", 'green', attrs=['bold']))
    print("########################################################################################")
    print("")
    print(colored(f"Welcome back, {name.upper()}", 'green', attrs=['bold']))

    print("Your Accounts:")

    stored_accounts = {}
    num = 0
    for account in password_data[email]["accounts"].keys():
        num += 1
        stored_accounts[num] = account
        print(f"Account {num}: {account}")

    print("")
    print("Enter the account number to retrieve password for")
    print("Enter 'N' to store password for a new account")
    print(colored("Enter 'D' to delete entry for a particular account", 'red', attrs=['bold']))
    print("Enter 'M' to go to account management page")
    print("Enter 'U' to update the password of an existing account")
    print("Enter 'H' to go to the Password Manager Help Menu")
    print(colored("Enter 'Q' to quit", 'blue', attrs=['bold']))

    while True:
        choice = input(">> ")
        # # code for retrieving password for selected account
        if choice.isdigit() and int(choice) <= num:
            password_retrieve(email, choice)

            break

        if choice.lower() == 'n':
            # code for creating new password
            password_store(email)
            break

        elif choice.lower() == 'm':
            # code for going to account management page
            account_management(email)
            break

        elif choice.lower() == 'u':
            update_password(email)
            break

        elif choice.lower() == 'q':
            # go to log out page
            sys.exit()

        elif choice.lower() == 'd':
            # delete the entry for a particular
            delete_password_entry(email)

        elif choice.lower() == 'h':
            help_menu(email)

        elif choice.lower() == 'l':
            logout(email)
        else:
            print("Invalid input. Please try again.")


def dict_printer(d):
    for k, v in d.items():
        if type(v) == dict:
            print(k)
            dict_printer(v)
        else:
            # print(colored(k, ': ', v, 'green', attrs=['bold']))
            print(colored(f"{k}:{v}", 'green', attrs=['bold']))


def register():
    _ = os.system('cls')
    print("########################################################################################")
    print(colored("PASSWORD MANAGER - REGISTER", 'green', attrs=['bold']))
    print("########################################################################################")
    global password_data
    print("Your choice: 2")
    print("--Register for a new account--")
    name = input('Please enter your name:\n>> ')
    email = input('Please enter your email:\n>>')

    while True:
        master_password = stdiomask.getpass(prompt='Please enter a master password:\n>> ')
        confirm_password = stdiomask.getpass(prompt='Re-enter a master password:\n>> ')
        if master_password != confirm_password:
            print("Passwords do not match. Please try again.")
        else:
            break

    # Store user data in password_data dictionary
    new_account = {
        "name": name,
        "master_password": master_password,
        "accounts": {}
    }

    password_data[email] = new_account

    # let the user know that registration is being completed and finally congratulate them
    print('Registering...')
    print(f"Congratulation, {name}. Your account has been successfully created.")
    _ = os.system('cls')
    show_dashboard(name, email, master_password)

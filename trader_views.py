#!/usr/bin/env python3

def login_or_register():
    user_input = input("""\n
Welcome to Terminal Trader!
Would you like to Login or Register? (L or R)
    \n"""
    )
    return user_input

def login():
    user_name_input = input("""\n
What is your username?
\n"""
    )
    user_password_input = input("""\n
What is your password?
\n"""
                            )
    if len(user_password_input) < 3 or len(user_password_input) < 3:
        return False, False
    else:
        return user_name_input, user_password_input


def register():
    user_name_reg_input = input("""\n
    What would you like as a username?
    \n"""
                            )
    user_password_reg_input = input("""\n
    What password do you prefer?
    \n"""
                                )
    if len(user_name_reg_input) < 3 or len(user_password_reg_input) <3:
        return False, False
    else:
        return user_name_reg_input, user_password_reg_input

def display_menu():
    user_input = input(
"""\n TERMINAL TRADER
Select an option:
(B) Buy Stock
(S) Sell Stock
(L) Look Up Symbol
(Q) Quote Symbol
(E) Exit Game\n"""
)
    return user_input

def buy_menu():
    user_input_buy_symbol = input("""What stock would you like to buy? Enter Symbol: \n""")
    return user_input_buy_symbol
def buy_quantity(price):
    user_input_get_quantity = input("""The price per share is {}. How many shares would you like to purchase? Enter quantity: \n""".format(price))
    return user_input_get_quantity
def confirm_buy():
    user_confirmation_to_buy = input("""Are you sure you wish to make this purchase? (Y or N)\n""")
    if user_confirmation_to_buy.upper() == 'Y':
        return True
    elif user_confirmation_to_buy.upper() == 'N':
        return False
    else:
        return None
def sell_menu():
    pass

def look_up_menu():
    user_company_look_up = input("""\n
                What company info would you like to look up? Enter company name: \n
                """)
    return user_company_look_up

def quote_symbol():
    user_input_symbol = input("""\n
            What stock quote would you like to look up? Enter symbol: \n""")
    return user_input_symbol

def pick_ticker_from_list(list_of_positions_message):
    print_dic = dict()
    for items in list_of_positions_message:
        print_dic[items[0]] = items[1:]
    print("Which of these stocks would you like to sell?")
    print_list = []
    for keys in print_dic:
        print_list.append(keys)
    print(print_list)
    user_input_symbol = input("""Enter symbol: \n""")
    if user_input_symbol in print_dic:
        # amount he can sell -> print_dic[user_input_symbol][1]
        # user picked a ticker he can sell, now we need to ask how many he would like to sell
        print("You can sell up to {} shares of stock".format(print_dic[user_input_symbol][1]))
        user_input_quantity = int(input("""How many would you like to sell?: \n"""))
        if user_input_quantity <= print_dic[user_input_symbol][1] and user_input_quantity > 0:
            return user_input_symbol ,user_input_quantity
        else:
            print("You can't sell that many shares")
    else:
        print('The ticker symbol you entered is not in your portfolio')

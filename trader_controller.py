#!/usr/bin/env python3
import time
import trader_models
import trader_views
import time
from operator import itemgetter

def menu_after_login(username):
    running = True
    while running:
        user_input = trader_views.display_menu()
        acceptable_inputs = ['P', 'B', 'S', 'L', 'Q', 'A', 'E']
        if user_input.upper() in acceptable_inputs:
            # EXIT option
            if user_input.upper() == "E":
                print("\nThank you for playing Terminal Trader!\n")
                running = False

            # PORTFOLIO OPTION
            elif user_input.upper() == "P":
                # go to models to go to ORM to access database for (1) Cash and (2) Stocks Owned Today
                # go to models to go to Wrapper to get fresh prices from API
                cash, stocks_today, name_price_dict = trader_models.get_cash_stocks_prices_snapshot(username)
                if stocks_today is False:
                    print("\n \nCash: ${}".format(cash))
                    print("You currently don't own any stocks in your portfolio")
                else:
                    print("\n \nYour current portfolio summary:")
                    print("Cash: ${}".format(cash))
                    for stocks in stocks_today:
                        print("Symb: {} ({})".format(stocks[0],stocks[2]))
                    NPV = 0
                    for stocks in stocks_today:
                        stock_q_times_p = float(stocks[2]) * float(name_price_dict[stocks[0]])
                        NPV += stock_q_times_p
                    NPV += float(cash)
                    print("Your portfolio is worth ${:.2f}".format(NPV))
                    NPVreturn = (NPV - 100000.0) / 100000.0
                    if NPVreturn >= 0:
                        print("Your portfolio is up {:.7f}%".format(NPVreturn))
                    else:
                        print("Your portfolio is down {:.7f}%".format(NPVreturn))

            elif user_input.upper() == "A":
                admin_password_response = trader_views.ask_for_admin_password()
                if admin_password_response == "root":
                    print("\nAccess granted - Creating Leaderboard Now...")
                    list_of_all_users = trader_models.get_all_users()
                    for persons in list_of_all_users:
                        time.sleep(2)
                        print('...')
                        cash, stocks_today, name_price_dict = trader_models.get_cash_stocks_prices_snapshot(persons[0])
                        if stocks_today is False:
                            persons.append(float(cash))
                        else:
                            NPV = 0.0
                            for stocks in stocks_today:
                                stock_q_times_p = float(stocks[2]) * float(name_price_dict[stocks[0]])
                                NPV += stock_q_times_p
                            NPV += float(cash)
                            persons.append(float(NPV))
                    leaderboard_list = sorted(list_of_all_users, key=itemgetter(1), reverse=True)
                    print('\n\n\n Leaderboard:')
                    for i in range(len(leaderboard_list)):
                        print("{}: {} ${}".format(i+1,leaderboard_list[i][0],leaderboard_list[i][1]))

                else:
                    print("\nAccess denied. Flee!")

            # BUY option
            elif user_input.upper() == "B":
                # get balance
                balance_message = trader_models.get_balance(username)
                if balance_message is False:
                    break
                else:
                    print("Your balance is {:.2f}".format(balance_message))
                # get desired buy symbol
                buy_symbol = trader_views.buy_menu()
                #check if symbol is real and return price
                check_symbol_exist_message = trader_models.get_quote(buy_symbol)
                if check_symbol_exist_message is None:
                    print("The stock symbol you entered may not exist")
                    break
                else:
                    # get quantity desired to buy
                    share_quantity = trader_views.buy_quantity(check_symbol_exist_message)
                    # check if user can afford quantity
                    cost = float(check_symbol_exist_message) * float(share_quantity)
                    difference = float(balance_message) - cost
                    if difference < 0:
                        print("You can't afford to buy that many shares")
                    else:
                        print("\n{} shares of {} will cost {:.2f}".format(share_quantity,buy_symbol,cost))
                        # confirm that user wants to actually buy
                        confirmation = None
                        while confirmation is None:
                            confirmation = trader_views.confirm_buy()
                        if confirmation is False:
                            continue
                        else:
                            # now that we know user wants to buy stock let's give it to him and deduct cost from balance
                            ################# CONTINUE HERE
                            trader_models.buy_stocks(share_quantity,buy_symbol,check_symbol_exist_message,username,balance_message)
            # SELL option
            elif user_input.upper() == "S":
                list_of_positions_message = trader_models.sell_list_of_positions(username)
                ticker_sell_symbol, ticker_sell_quantity = trader_views.pick_ticker_from_list(list_of_positions_message)
                trader_models.sell_stocks(username, ticker_sell_symbol, ticker_sell_quantity)

            # LOOK UP option
            elif user_input.upper() == "L":
                get_look_up_input = trader_views.look_up_menu()
                company_name, company_exchange, company_ticker = trader_models.look_up(get_look_up_input)
                if company_name is False:
                    print("{} is not a valid search result and may not be publicly traded stock".format(get_look_up_input))
                else:
                    print("{}, known as {}, is listed on the {} as {}".format(get_look_up_input, company_name, company_exchange, company_ticker))

            # get QUOTE option
            elif user_input.upper() == "Q":
                print("Quote")
                # get user input
                get_quote = trader_views.quote_symbol()
                lookupquote_price = trader_models.get_quote(get_quote)
                if lookupquote_price is None:
                    print("Hmm... your stock does not exist")
                else:
                    print("\nStock symbol {} is worth ${}".format(get_quote.upper(), lookupquote_price))

            else:
                print("Something is broken")
        else:
            print("Hmm.. That is not acceptable input")

def login_or_register():
    bad_input = True
    while bad_input:
        user_input = trader_views.login_or_register()
        acceptable_inputs = ['L','R']
        if user_input.upper() in acceptable_inputs:
            if user_input.upper() == 'L':
                login_username, login_password = trader_views.login()
                if login_username is False or login_password is False:
                    print("Your login attempt failed. The username/password is not up to par...")
                    break
                login_attempt_return_message, second_return_message = trader_models.login(login_username, login_password)
                if login_attempt_return_message is not False:
                    print("Welcome '{}', you are logged in. Your current balance is '{}'.".format(login_attempt_return_message, second_return_message))
                    menu_after_login(login_username)
                    break
                else:
                    print("Your login attempt failed. The username/password does not exist...")
                    break

            elif user_input.upper() == 'R':
                register_username, register_password = trader_views.register()
                if register_username is False or register_password is False:
                    print("Your registration attempt failed. The username/password is not up to par...")
                    break
                register_attempt = trader_models.register(register_username,register_password)
                if register_attempt:
                    print("\nRegistration successful!")
                    continue
                else:
                    print('Registration attempt broken')
            else:
                print('login/register question broken')
        else:
            print('Hmm.. Invalid option')





if __name__ == "__main__":
    login_or_register()


#!/usr/bin/env python3 

import orm
import wrapper

def buy(symbol):
    pass

    # def tell_ORM_to_make_changes_in_DB(symbol):
    #     pass

def look_up(symbol):
    company_name, company_exchange, company_symbol = wrapper.get_company_info(symbol)
    return company_name, company_exchange, company_symbol

def get_quote(symbol):
    # get data on symbol from wrapper who gets data from API
    stock_name_price_list = wrapper.get_stock_price(symbol)
    if stock_name_price_list[0] is not None:
        return stock_name_price_list[1]
    else:
        return None


def register(username, password):
    insert_into_DB_attempt = orm.register(username,password)
    if insert_into_DB_attempt:
        return True
    else:
        return False

def login(username, password):
    query_attemp_success, username_from_db, current_balance = orm.login(username,password)
    if query_attemp_success is True:
        return username_from_db, current_balance
    else:
        return False, False

def get_balance(username):
    balance_message = orm.get_balance(username)
    return balance_message

def buy_stocks(quantity,ticker,price,username, balance):
    # change balance to subtract cost of new shares. True means it worked. Else False.
    update_balance_message = orm.buy_stocks_users_table(quantity,price,username,balance)
    if update_balance_message is not False:
        # insert data into transactions to show that user bought shares
        update_transactions_message = orm.buy_stocks_transactions_table(quantity,ticker,price,username)
        if update_transactions_message is not False:
            # check if position on shares exist, if so change position, else add position
            update_positions_message = orm.buy_stocks_positions_table(quantity,ticker,price,username, balance)
        else:
            return False
    else:
        return False
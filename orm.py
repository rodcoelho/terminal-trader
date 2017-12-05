import sqlite3
import datetime

connection = sqlite3.connect('stocktrade.db')
cursor = connection.cursor()

def register(username,password):
    connection = sqlite3.connect('stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
INSERT INTO users(name, password, balance)
VALUES ('{}','{}',10000);
    """.format(username,password))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        connection.commit()
        cursor.close()
        connection.close()
        return False

def login(username,password):
    connection = sqlite3.connect('stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
    SELECT name, balance
    FROM users
    WHERE name = '{}' AND password = '{}';
        """.format(username, password))
        fetch = cursor.fetchall()
        try:
            connection.commit()
            cursor.close()
            connection.close()
            return True, fetch[0][0], fetch[0][1]
        except:
            connection.commit()
            cursor.close()
            connection.close()
            return False, False, False
    except:
        connection.commit()
        cursor.close()
        connection.close()
        return False, False, False

def get_balance(username):
    connection = sqlite3.connect('stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT balance
        FROM users
        WHERE name = '{}'
        ;
            """.format(username))
        fetch = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return fetch[0]
    except:
        connection.commit()
        cursor.close()
        connection.close()
        return False

def buy_stocks_users_table(quantity,price,username,balance):
    connection = sqlite3.connect('stocktrade.db')
    cursor = connection.cursor()

    # update the balance in the USERS table to show that he bought shares
    cost = float(quantity) * float(price)
    difference = float(balance) - cost

    try:
        cursor.execute("""
            UPDATE users SET balance = '{}' WHERE name = '{}'
            ;
                """.format(difference,username))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        connection.commit()
        cursor.close()
        connection.close()
        return False

def buy_stocks_transactions_table(quantity,ticker,price,username):
    connection = sqlite3.connect('stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
        SELECT pk FROM users WHERE name = '{}'
                    ;
                        """.format(username))
    id = cursor.fetchone()
    now = datetime.datetime.now()

    # update the TRANSACTIONS table to show that he bought shares
    try:
        cursor.execute("""
                INSERT INTO transactions(userID, symbol, unixtime, lastprice, quantity, buysell)
                VALUES ('{}','{}','{}','{}','{}','{}')
                ;
                    """.format(id[0],ticker,now,price, quantity,'b' ))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        connection.commit()
        cursor.close()
        connection.close()
        return False

def buy_stocks_positions_table(quantity,ticker,price,username, balance):
    connection = sqlite3.connect('stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
            SELECT pk FROM users WHERE name = '{}'
                        ;
                            """.format(username))
    id = cursor.fetchone()

    # check if anything in positions exists. If so create VWAP and then UPDATE. Else add to positions.
    cursor.execute("""
            SELECT VWAP, quantity
            FROM positions
            WHERE userID = '{}' AND symbol = '{}';
                        """.format(id[0], ticker))
    VWAP_query = cursor.fetchall()

    # if VWAP doesn't exist in positions list then add to positions
    if len(VWAP_query) == 0:
        # check if initial commit of symbol to position - if so we can add to position'
        cursor.execute("""
                INSERT INTO positions(userID, symbol, quantity, VWAP)
                VALUES('{}','{}','{}','{}')
                ;""".format(id[0], str(ticker), quantity, float(price)))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        # stock already in position - time to adjust the position
        VWAP_price = VWAP_query[0][0]
        VWAP_quantity = VWAP_query[0][1]
        newVWAPtop = (float(price) * float(quantity)) + (float(VWAP_price) * float(VWAP_quantity))
        newVWAPbottom = (float(VWAP_quantity) + float(quantity))
        VWAP_price = float(newVWAPtop) / float(newVWAPbottom)
        VWAPfinalprice = VWAP_price
        VWAPfinalquantity = newVWAPbottom
        print("VWAP price should now be {}".format(VWAPfinalprice))
        print("VWAP quantity should now be {}".format(VWAPfinalquantity))

        # update quantity
        cursor.execute("""
        UPDATE positions
        SET quantity = '{}'
        WHERE userID = '{}' AND symbol = '{}'
        ;""".format(int(VWAPfinalquantity), id[0], ticker))

        connection.commit()

        # update VWAPprice
        cursor.execute("""
                UPDATE positions
                SET VWAP = '{}'
                WHERE userID = '{}' AND symbol = '{}'
                ;""".format(VWAPfinalprice, id[0], ticker))

        connection.commit()

        VWAP_query = cursor.fetchall()
        print(VWAP_query)

        connection.commit()
        cursor.close()
        connection.close()
import pandas as pd
import numpy as np
import sqlite3 as sql
import hashlib
from flask import Flask
from flask import request, jsonify

database = "./database.db"
userTable = "LionAuctionDataset-v3/Users.csv"

def init_user_table():
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Users (email CHAR(60), password CHAR(60),
                        PRIMARY KEY(email));"""
        cursor.execute(create_table)

        # load users csv from data files
        users = pd.read_csv(userTable)

        # encrypt password using sha256
        users["password"] = users["password"].apply(lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest())

        # upload table to sql using Pandas to_sql
        users[["email", "password"]].to_sql("Users", con=conn, if_exists="append", index=False)
        conn.commit()

    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()




if __name__ == "__main__":
    init_user_table()





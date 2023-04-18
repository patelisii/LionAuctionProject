import pandas as pd
import sqlite3 as sql
import hashlib

database = "backend/database.db"
userTable = "LionAuctionDataset-v5/Users.csv"
bidderTable = "LionAuctionDataset-v5/Bidders.csv"

def init_UserPass_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE UserPass (email CHAR(60), password CHAR(60),
                        PRIMARY KEY(email));"""
        cursor.execute(create_table)

        # load users csv from data files
        users = pd.read_csv(file_path)

        # encrypt password using sha256
        users["password"] = users["password"].apply(lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest())

        # upload table to sql using Pandas to_sql
        users[["email", "password"]].to_sql("UserPass", con=conn, if_exists="append", index=False)
        conn.commit()

    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()


def init_Bidders_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Bidders (
                        email CHAR(60), 
                        first_name CHAR(60),
                        last_name CHAR(60),
                        gender CHAR(60), 
                        age INT,
                        home_address_id CHAR(60),
                        major CHAR(20),
                        FOREIGN KEY (email) REFERENCES UserPass (email),
                        FOREIGN KEY (home_address_id) REFERENCES Address (address_id),
                        PRIMARY KEY (email));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Bidders", con=conn, if_exists="append", index=False)
        conn.commit()

    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_Address_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Address (
                        address_id CHAR(60), 
                        zipcode CHAR(10),
                        street_num CHAR(10),
                        street_name CHAR(60), 
                        FOREIGN KEY (zipcode) REFERENCES ZipCode (zipcode),
                        PRIMARY KEY (address_id));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Address", con=conn, if_exists="append", index=False)
        conn.commit()
        conn.close()

    except sql.Error as error:
        print(error)

def init_ZipCode_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE ZipCode (
                        zipcode CHAR(10), 
                        city CHAR(60),
                        state CHAR(60),
                        PRIMARY KEY (zipcode));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("ZipCode", con=conn, if_exists="append", index=False)
        conn.commit()
        conn.close()

    except sql.Error as error:
        print(error)


def init_Sellers_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Sellers (
                        email Char(60), 
                        bank_routing_number CHAR(60),
                        bank_account_number CHAR(60),
                        balance REAL, 
                        FOREIGN KEY (email) REFERENCES UserPass (email),
                        PRIMARY KEY (email));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Sellers", con=conn, if_exists="append", index=False)
        conn.commit()

    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_LocalVendors_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE LocalVendors (
                        email Char(60), 
                        Business_Name CHAR(60),
                        Business_Address_ID CHAR(60),
                        Customer_Service_Phone_Number CHAR(12), 
                        FOREIGN KEY (email) REFERENCES UserPass (email),
                        FOREIGN KEY (Business_Address_ID) REFERENCES Address (address_id),
                        PRIMARY KEY (email));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("LocalVendors", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_Helpdesk_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Helpdesk (
                        email Char(60), 
                        Position CHAR(60),
                        FOREIGN KEY (email) REFERENCES UserPass (email),
                        PRIMARY KEY (email));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Helpdesk", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_CreditCards_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE CreditCards (
                        owner_email Char(60), 
                        credit_card_num CHAR(20),
                        card_type CHAR(60),
                        expire_month INT, 
                        expire_year INT,
                        security_code CHAR(3),
                        FOREIGN KEY (owner_email) REFERENCES Bidders (email),
                        PRIMARY KEY (credit_card_num));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("CreditCards", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_Bids_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Bids (
                        Bid_ID INT, 
                        Seller_Email CHAR(60),
                        Listing_ID INT,
                        Bidder_Email CHAR(60), 
                        Bid_Price REAL,
                        FOREIGN KEY (Seller_Email) REFERENCES Sellers (email),
                        FOREIGN KEY (Bidder_Email) REFERENCES Bidders (email),
                        FOREIGN KEY (Listing_ID) REFERENCES Auction_Listings (Listing_ID),
                        PRIMARY KEY (Bid_ID));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Bids", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_Auction_Listings_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Auction_Listings (
                        Seller_Email CHAR(60),
                        Listing_ID INT,
                        Category CHAR(60), 
                        Auction_Title VARCHAR(255),
                        Product_Name VARCHAR(255),
                        Product_Description VARCHAR(255),
                        Quantity INT,
                        Reserve_Price CHAR(10),
                        Max_bids INT,
                        Status BOOL,
                        FOREIGN KEY (Seller_Email) REFERENCES Sellers (email),
                        FOREIGN KEY (Category) REFERENCES Categories (category_name),
                        PRIMARY KEY (Listing_ID, Seller_Email));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Auction_Listings", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_Categories_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Categories (
                        parent_category CHAR(60),
                        category_name CHAR(60),
                        PRIMARY KEY (category_name));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Categories", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()


def init_Ratings_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Ratings (
                        Bidder_Email CHAR(60),
                        Seller_Email CHAR(60),
                        Date DATE,
                        Rating INT, 
                        Rating_Desc VARCHAR(255),
                        FOREIGN KEY (Bidder_Email) REFERENCES Bidders (email),
                        FOREIGN KEY (Seller_Email) REFERENCES Sellers (email),
                        PRIMARY KEY (Bidder_Email, Seller_Email, Date));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Ratings", con=conn, if_exists="append", index=False)
        conn.commit()
        conn.close()
    except sql.Error as error:
        print(error)


def init_Requests_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Requests (
                        Request_id INT,
                        sender_email CHAR(60),
                        helpdesk_staff_email CHAR(60),
                        request_type CHAR(60), 
                        request_desc VARCHAR(255),
                        request_status BOOL,
                        FOREIGN KEY (sender_email) REFERENCES UserPass (email),
                        FOREIGN KEY (helpdesk_staff_email) REFERENCES Helpdesk (email),
                        PRIMARY KEY (request_id));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Requests", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def init_Transactions_table(file_path):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()

        # SQL query for creating user table
        create_table = """CREATE TABLE Transactions (
                        Transaction_ID INT,
                        Seller_Email CHAR(60),
                        Listing_ID INT,
                        Bidder_Email CHAR(60),
                        Date DATE,
                        Payment REAL, 
                        FOREIGN KEY (Bidder_Email) REFERENCES Bidders (email),
                        FOREIGN KEY (Seller_Email) REFERENCES Sellers (email),
                        FOREIGN KEY (Listing_ID) REFERENCES Auction_Listings (Listing_ID),
                        PRIMARY KEY (Transaction_ID));"""
        cursor.execute(create_table)

        # load users csv from data files
        table = pd.read_csv(file_path)

        # upload table to sql using Pandas to_sql
        table.to_sql("Transactions", con=conn, if_exists="append", index=False)
        conn.commit()
    except sql.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    pass
    # user Tables
    # init_UserPass_table(file_path="LionAuctionDataset-v5/Users.csv")
    init_ZipCode_table(file_path="LionAuctionDataset-v5/Zipcode_info.csv")
    init_Address_table(file_path="LionAuctionDataset-v5/Address.csv")
    # init_Bidders_table(file_path="LionAuctionDataset-v5/Bidders.csv")
    # init_CreditCards_table(file_path="LionAuctionDataset-v5/Credit_Cards.csv")
    # init_Sellers_table(file_path="LionAuctionDataset-v5/Sellers.csv")
    # init_LocalVendors_table(file_path="LionAuctionDataset-v5/Local_Vendors.csv")
    #
    # # Auction tables
    # init_Categories_table(file_path="LionAuctionDataset-v5/Categories.csv")
    # init_Auction_Listings_table(file_path="LionAuctionDataset-v5/Auction_Listings.csv")
    # init_Transactions_table(file_path="LionAuctionDataset-v5/Transactions.csv")
    # init_Ratings_table(file_path="LionAuctionDataset-v5/Ratings.csv")
    # init_Bids_table(file_path="LionAuctionDataset-v5/Bids.csv")
    #
    # # Helpdesk tables
    # init_Helpdesk_table(file_path="LionAuctionDataset-v5/Helpdesk.csv")
    # init_Requests_table(file_path="LionAuctionDataset-v5/Requests.csv")
















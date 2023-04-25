import sqlite3 as sql
import pandas as pd

database = "backend/database.db"

def get_products_by_category(category):
    conn = sql.connect(database)

    cat = f"'{category}'"

    listings = pd.read_sql(f"SELECT * FROM Auction_Listings a WHERE a.Category={cat} AND a.Status=1;", conn)
    return listings.to_dict(orient='records')

def get_topLevel_categories():
    return get_child_categories("Root")

def get_child_categories(category):
    conn = sql.connect(database)

    cat = f"'{category}'"

    cats = pd.read_sql(f"SELECT * FROM Categories c WHERE c.parent_category={cat};", conn)
    return cats["category_name"].to_list()

def get_parent(category):
    conn = sql.connect(database)

    cat = f"'{category}'"

    cats = pd.read_sql(f"SELECT * FROM Categories c WHERE c.category_name={cat};", conn)
    return cats["parent_category"].to_list()

def get_seller_listings(sellerEmail):
    conn = sql.connect(database)

    email = f"'{sellerEmail}'"

    listings = pd.read_sql(f"SELECT * FROM Auction_Listings a WHERE a.Seller_Email={email} AND a.Status!=0 ORDER BY Status ASC;", conn)
    return listings.to_dict(orient='records')

def update_auction_listing(listing_id, new_values):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE auction_listings
        SET
          Auction_Title = ?,
          Product_Name = ?,
          Product_Description = ?,
          Category = ?,
          Quantity = ?,
          Reserve_Price = ?,
          Max_bids = ?,
          Status = ?
        WHERE Listing_ID = ?
    """, (
        new_values['Auction_Title'],
        new_values['Product_Name'],
        new_values['Product_Description'],
        new_values['Category'],
        new_values['Quantity'],
        new_values['Reserve_Price'],
        new_values['Max_bids'],
        new_values['Status'],
        listing_id,
    ))

    conn.commit()
    conn.close()

def get_next_listing_id():
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(Listing_ID) FROM Auction_Listings")
    max_id = cursor.fetchone()[0]

    conn.close()

    return max_id + 1

def insert_auction_listing(listing):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Auction_listings (
            Listing_ID, Seller_Email, Auction_Title, Product_Name, Product_Description,
            Category, Quantity, Reserve_Price, Max_bids, Status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        listing['Listing_ID'], listing['Seller_Email'], listing['Auction_Title'],
        listing['Product_Name'], listing['Product_Description'], listing['Category'],
        listing['Quantity'], listing['Reserve_Price'], listing['Max_bids'], listing['Status']
    ))

    conn.commit()
    conn.close()

def highest_bid(listing_id):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT Bid_ID, Seller_Email, Listing_ID, Bidder_Email, MAX(Bid_Price) as Bid_Price FROM Bids b WHERE b.Listing_ID = ?;", (listing_id, ))
    row = cursor.fetchone()
    max_bid = {"Bid_ID": row[0], "Seller_Email": row[1], "Listing_ID": row[2], "Bidder_Email": row[3], "Bid_Price": row[4]}

    conn.close()

    return max_bid

def auction_listing_by_id(listing_id):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Auction_Listings a WHERE a.Listing_ID = ?;", (listing_id,))
    row = cursor.fetchone()

    auction_listing = {"Seller_Email": row[0],
                       "Listing_ID": row[1],
                       "Category": row[2],
                       "Auction_Title": row[3],
                       "Product_Name": row[4],
                       "Product_Description": row[5],
                       "Quantity": row[6],
                       "Reserve_Price":row[7],
                       "Max_bids": row[8],
                       "Status": row[9]}
    conn.close()

    return auction_listing

def all_bids(listing_id):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT Bid_ID, Seller_Email, Listing_ID, Bidder_Email, Bid_Price FROM Bids b WHERE b.Listing_ID = ? ORDER BY Bid_Price DESC;", (listing_id,))
    rows = cursor.fetchall()

    bids = [{"Bid_ID": row[0], "Seller_Email": row[1], "Listing_ID": row[2], "Bidder_Email": row[3], "Bid_Price": row[4]} for row in rows]

    conn.close()

    return bids

def get_next_bid_id():
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(Bid_ID) FROM Bids")
    max_id = cursor.fetchone()[0]

    conn.close()

    return max_id + 1

def place_bid(bid):

    # check max bids
    listing = auction_listing_by_id(bid["Listing_ID"])
    bids = all_bids(bid["Listing_ID"])
    if listing["Max_bids"] == len(bids):
        return "Over bid limit"

    # check if previous bid was same user
    last = highest_bid(bid["Listing_ID"])
    if last["Bidder_Email"] is not None:
        if last["Bidder_Email"] == bid["Bidder_Email"]:
            return "User cannot bid twice in a row"

        # check bid amount is 1 dollar higher
        if bid["Bid_Price"]-last["Bid_Price"] < 1:
            return "Bid not $1 higher than previous bid"

    conn = sql.connect(database)
    cursor = conn.cursor()

    new_bid_id = get_next_bid_id()

    cursor.execute("""
            INSERT INTO Bids (
                Bid_ID, Seller_Email, Listing_ID, Bidder_Email, Bid_Price
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
        new_bid_id, bid['Seller_Email'], bid['Listing_ID'],
        bid['Bidder_Email'], bid['Bid_Price']
    ))

    conn.commit()
    conn.close()

    # check auction over
    listing = auction_listing_by_id(bid["Listing_ID"])
    bids = all_bids(bid["Listing_ID"])
    if listing["Max_bids"] == len(bids):
        # make auction invalid regardless
        soldListing = listing.copy()
        soldListing["Status"] = 0
        update_auction_listing(listing["Listing_ID"], soldListing)
        return "Last Bid"

    return "Success"

def get_credit_card(email):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM CreditCards c WHERE c.owner_email=?;", (email, ))
    card = cursor.fetchone()

    conn.close()

    exp = f'{card[3]}/{card[4]}'
    info = [card[1], exp, card[5]]


    return info

def get_next_transaction_id():
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(Transaction_ID) FROM Transactions")
    max_id = cursor.fetchone()[0]

    conn.close()

    return max_id + 1

def get_bid_by_id(bid_id):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Bid_ID, Seller_Email, Listing_ID, Bidder_Email, MAX(Bid_Price) as Bid_Price FROM Bids b WHERE b.Bid_ID = ?;",
        (bid_id,))
    row = cursor.fetchone()
    bid = {"Bid_ID": row[0], "Seller_Email": row[1], "Listing_ID": row[2], "Bidder_Email": row[3],
               "Bid_Price": row[4]}

    conn.close()

    return bid

def complete_transaction(bid_id):
    conn = sql.connect(database)
    cursor = conn.cursor()

    bid = get_bid_by_id(bid_id)
    id = get_next_transaction_id()

    import datetime

    date = datetime.date.today()

    print(date)

    cursor.execute("""
            INSERT INTO Transactions (
                Transaction_ID, Seller_Email, Listing_ID, Bidder_Email, Date, Payment
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
        id, bid['Seller_Email'], bid['Listing_ID'],
        bid['Bidder_Email'], date, bid['Bid_Price']
    ))

    conn.commit()
    conn.close()

    listing = auction_listing_by_id(bid["Listing_ID"])
    soldListing = listing.copy()
    soldListing["Status"] = 2
    update_auction_listing(listing["Listing_ID"], soldListing)

def cancel_auction(listing_id, reason):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
                INSERT INTO Canceled_Listings (
                    Listing_ID, Reason
                )
                VALUES (?, ?)
            """, (
        listing_id, reason
    ))

    conn.commit()
    conn.close()


def update_profile(email, newData):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
            UPDATE Bidders
            SET
              first_name = ?,
              last_name = ?,
              gender = ?,
              age = ?,
              major = ?
            WHERE email = ?
        """, (
        newData['firstName'],
        newData['lastName'],
        newData['gender'],
        newData['age'],
        newData['major'],
        email,
    ))

    conn.commit()
    conn.close()

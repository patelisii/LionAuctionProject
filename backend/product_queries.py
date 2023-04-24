import sqlite3 as sql
import pandas as pd

database = "lion-auction/backend/database.db"

def get_products_by_category(category):
    conn = sql.connect(database)

    cat = f"'{category}'"

    listings = pd.read_sql(f"SELECT * FROM Auction_Listings a WHERE a.Category={cat};", conn)
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

    listings = pd.read_sql(f"SELECT * FROM Auction_Listings a WHERE a.Seller_Email={email};", conn)
    return listings.to_dict(orient='records')

def update_auction_listing(listing_id, new_values):
    conn = sql.connect(database)
    cursor = conn.cursor()

    print("""UPDATE auction_listings
        SET
          Auction_Title = ?,
          Product_Name = ?,
          Product_Description = ?,
          Category = ?,
          Quantity = ?,
          Reserve_Price = ?,
          Max_bids = ?,
          Status = ?
        WHERE (Listing_ID, Seller_Email) = ?
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

    return max_id + 1 if max_id else 1

def insert_auction_listing(listing):
    conn = sql.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO auction_listings (
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
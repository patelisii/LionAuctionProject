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

# get_topLevel_categories()
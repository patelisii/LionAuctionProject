from flask import Flask
from flask_cors import CORS

import pandas as pd
import sqlite3 as sql
import hashlib
from flask import Flask
from flask import request, jsonify
import user_queries
import product_queries

app = Flask(__name__)
CORS(app)

database = "lion-auction/backend/database.db"

@app.route('/login', methods=['POST'])
def login_attempt():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        type = data.get('userType')

        conn = sql.connect(database)
        cursor = conn.cursor()

        # check if user is in correct Table
        type_check=""
        if type == 'Bidder':
            type_check = "SELECT email FROM Bidders WHERE email=?"
        elif type == 'Seller':
            type_check = "SELECT email FROM Sellers WHERE email=?"
        elif type == 'Local Business':
            type_check = "SELECT email FROM LocalVendors WHERE email=?"
        else:
            type_check = "SELECT email FROM Helpdesk WHERE email=?"

        cursor.execute(type_check, (email,))
        found = cursor.fetchone()
        if found==None:
            return jsonify({"message": f"Email not found in {type} database"}), 401

        # search if an account with email exists
        get_user = "SELECT email, password FROM UserPass WHERE email=?"
        cursor.execute(get_user, (email,))

        hashpass = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user = cursor.fetchone()
        if user == None:
            return jsonify({"message": "Invalid email address"}), 404
        elif hashpass != user[1]:
            return jsonify({"message": "Incorrect password"}), 401
        else:
            return jsonify({"message": "Login successful"}), 200
        conn.commit()
        conn.close()
    except sql.Error as error:
        return jsonify({"message": "Error connecting to database"}), 405


@app.route('/get_profile', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('email')
    user_type = data.get('userType')
    user_data_dict = user_queries.get_profile_data(email, user_type)
    return jsonify(user_data_dict)

@app.route('/get_products_by_category', methods=['POST'])
def fetch_product_cat():
    data = request.get_json()
    category = data['category']
    print(f"Fetching auction listings for {category}...")
    listings = product_queries.get_products_by_category(category)

    # print(listings)
    return jsonify(listings)

@app.route('/get_topLevel_categories', methods=['GET'])
def top_cats():
    print("Fetching top categories...")
    cats = product_queries.get_topLevel_categories()
    # cats is a list of category names

    # print(cats)
    return cats

@app.route('/get_child_categories', methods=['POST'])
def child_cats():
    data = request.get_json()
    category = data['category']
    print(f"Fetching child categories for {category}...")
    # cats is a list of category names
    cats = product_queries.get_child_categories(category)
    # print(cats)
    return cats

@app.route('/get_parent_category', methods=['POST'])
def parent_cat():
    data = request.get_json()
    category = data['category']
    print(f"Fetching parent category for {category}...")
    parent = product_queries.get_parent(category)
    # print(parent)
    return parent

@app.route('/get_seller_listings', methods=['POST'])
def seller_listings():
    data = request.get_json()
    email = data['email']
    listings = product_queries.get_seller_listings(email)
    print(listings)
    return jsonify(listings)

@app.route("/update_auction_listing", methods=['POST'])
def update_listing():
    data = request.get_json()
    listing_id = data['listing_id']
    new_values = data['new_values']

    try:
        product_queries.update_auction_listing(listing_id, new_values)
        return jsonify({"success": True, "message": "Auction listing updated successfully."}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"success": False, "message": "Failed to update auction listing."}), 500

@app.route('/create_auction_listing', methods=['POST'])
def create_listing():
    data = request.get_json()
    listing = data['listing']

    try:
        listing_id = product_queries.get_next_listing_id()
        listing['Listing_ID'] = listing_id
        product_queries.insert_auction_listing(listing)
        return jsonify({"success": True, "message": "Auction listing created successfully.", "listing_id": listing_id}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"success": False, "message": "Failed to create auction listing."}), 500


if __name__ == '__main__':
    app.run()

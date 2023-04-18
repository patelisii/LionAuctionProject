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

    print(listings)
    return jsonify(listings)

@app.route('/get_topLevel_categories', methods=['GET'])
def top_cats():
    print("Fetching top categories...")
    cats = product_queries.get_topLevel_categories()
    # cats is a list of category names

    print(cats)
    return cats

@app.route('/get_child_categories', methods=['POST'])
def child_cats():
    data = request.get_json()
    category = data['category']
    print(f"Fetching child categories for {category}...")
    # cats is a list of category names
    cats = product_queries.get_child_categories(category)
    print(cats)
    return cats


if __name__ == '__main__':
    app.run()

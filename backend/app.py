from flask import Flask
from flask_cors import CORS

import pandas as pd
import sqlite3 as sql
import hashlib
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)
CORS(app)

database = "database.db"
userTable = "LionAuctionDataset-v3/Users.csv"


@app.route('/login', methods=['POST'])
def login_attempt():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = sql.connect(database)
        print("Connection Successful")
        cursor = conn.cursor()

        # search if an account with email exists
        get_user = "SELECT email, password FROM Users WHERE email=?"
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
    except sql.Error as error:
        return jsonify({"message": "Error connecting to database"}), 405
    finally:
        if conn:
            conn.close()




if __name__ == '__main__':
    app.run()

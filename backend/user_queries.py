import sqlite3 as sql

database = "backend/database.db"


def get_profile_data(email, user_type):
    conn = sql.connect(database)  # Replace with your database connection
    cursor = conn.cursor()

    user_data_dict = {}

    if user_type == 'Bidder':
        cursor.execute("""SELECT email, first_name, last_name, gender, age, major, street_num, street_name, city, state, z.zipcode AS zip, credit_card_num FROM
                 ((((SELECT * FROM Bidders WHERE email=?) person JOIN
                     Address a ON person.home_address_id=a.address_id) pa JOIN
                        ZipCode z ON pa.zipcode=z.zipcode) paz JOIN
                            CreditCards c ON c.owner_email=paz.email);""", (email,))
        user_data = cursor.fetchone()
        address = user_data[6] + " " + user_data[7] + ", " + user_data[8] + ", " + user_data[9] + " " + user_data[10]
        card = user_data[11][-4:]
        # Convert the query result to a dictionary
        user_data_dict = {
            'email': user_data[0],
            'firstName': user_data[1],
            'lastName': user_data[2],
            'gender': user_data[3],
            'age': user_data[4],
            'major': user_data[5],
            'address': address,
            'cardDigits': card

        }

    elif user_type == 'Seller':
        cursor.execute("""SELECT a.email, first_name, last_name, gender, age, major,
               street_num, street_name, city, state, z.zipcode AS zip, credit_card_num,
               balance, bank_routing_number, bank_account_number FROM
                     ((((SELECT * FROM Bidders WHERE email=?) person JOIN
                         Address a ON person.home_address_id=a.address_id) pa JOIN
                            ZipCode z ON pa.zipcode=z.zipcode) paz JOIN
                                CreditCards c ON c.owner_email=paz.email) a JOIN Sellers s ON a.email=s.email;""",
                       (email,))
        user_data = cursor.fetchone()
        address = user_data[6] + " " + user_data[7] + ", " + user_data[8] + ", " + user_data[9] + " " + user_data[10]
        card = user_data[11][-4:]
        # Convert the query result to a dictionary
        user_data_dict = {
            'email': user_data[0],
            'firstName': user_data[1],
            'lastName': user_data[2],
            'gender': user_data[3],
            'age': user_data[4],
            'major': user_data[5],
            'address': address,
            'cardDigits': card,
            'balance': user_data[12],
            'bankRoutingNumber': user_data[13],
            'bankAccountNumber': user_data[14]
        }

    elif user_type == 'Local Business':
        cursor.execute("""SELECT s.email, Business_Name, Customer_Service_Phone_Number,
               street_num, street_name, city, state, paz.zipcode,
               balance, bank_routing_number, bank_account_number
                FROM ((SELECT * FROM (SELECT * FROM LocalVendors WHERE email=?) Business JOIN
                    Address a ON Business.Business_Address_ID=a.address_id) pa JOIN
                        ZipCode z ON pa.zipcode=z.zipcode) paz JOIN Sellers s ON paz.email=s.email;""", (email,))

        user_data = cursor.fetchone()
        address = user_data[3] + " " + user_data[4] + ", " + user_data[5] + ", " + user_data[6] + " " + user_data[7]
        # Convert the query result to a dictionary
        user_data_dict = {
            'email': user_data[0],
            'businessName': user_data[1],
            'customerServiceNumber': user_data[2],
            'address': address,
            'balance': user_data[8],
            'bankRoutingNumber': user_data[9],
            'bankAccountNumber': user_data[10],
        }

    elif user_type == 'Helpdesk':

        cursor.execute("""SELECT paz.email, first_name, last_name, gender, age, major, 
               street_num, street_name, city, state, z.zipcode AS zip, credit_card_num, Position FROM
                     (((SELECT * FROM (SELECT * FROM Bidders bb JOIN Helpdesk H on bb.email = H.email)
                                 WHERE email=?) person JOIN
                         Address a ON person.home_address_id=a.address_id) pa JOIN
                            ZipCode z ON pa.zipcode=z.zipcode) paz JOIN
                                CreditCards c ON c.owner_email=paz.email;""", (email,))
        user_data = cursor.fetchone()
        address = user_data[6] + " " + user_data[7] + ", " + user_data[8] + ", " + user_data[9] + " " + user_data[10]
        card = user_data[11][-4:]
        # Convert the query result to a dictionary
        user_data_dict = {
            'email': user_data[0],
            'firstName': user_data[1],
            'lastName': user_data[2],
            'gender': user_data[3],
            'age': user_data[4],
            'major': user_data[5],
            'address': address,
            'cardDigits': card,
            'position': user_data[12]

        }

    conn.close()
    return user_data_dict
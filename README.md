# Lion Auction Phase 2 Progress Review

## Context

### Frontend

The frontend was made with React JS. This project also implements Material UI, a plugin used for modals and styling throughout the app. 

### Backend

The backend was made with Python and Flask and serves RESTFul APIs to the frontend. All of the flask API functions are in app.py. Helper functions for querying the database are located in user_queries.py and product_queries.py. The data_upload.py file contains the scripts for initializing the database tables and uploading all the data from the provided CSV files. 

### Database

This project uses SQLite3 as the database. All queries to the database are in the python flask backend.

## Features 
This app supports the following features for bidders:
- Logging in as a bidder, seller, local business, or helpdesk employee
- Browsing auction listings by category and traversing the category hierarchy
- Selecting on an auction listing to view more details and current bids
- Placing a bid on an auction listing
- Winning an auction and completing a transaction
- View profile information
- Edit profile information

This app supports the following features for sellers and local vendors:
- View and edit auction listings
- Cancel an auction
- Create a new listing

## Organization 

There are two major parts to this system. The backend folder contains the python files and database file. The app.py is the main file and must be run to launch the backend. It runs functions from the product_queries.py and user_queries.py. 

All of the frontend code is located in the src folder. As traditional for React projects, the main files are the App.js and Index.js which initialize the app, the app state variables and routes to each page.  

All of the web page JavaScript files are located in the components folder in src. Some of the files have CSS files for adding style. For most of the UX, the user is on the Main.js page. Depending on the user, this page shows catgeory and auction browsing (CategoryView.js and AuctionDetails.js), as well as showing sellers their auction listings and letting sellers edit them (SellerListings.js). UserContext intializes the context variables for the app, userType and userEmail, which are used throughout the app for various use cases. 

## Instructions 
Note: if you opened this file in Pycharm, you can run these bash command blocks in the Readme view

Open the lion-auction folder to get started. Make sure your terminal remains in this folder for this entire tutorial. First make sure you have python, npm, and Node.js installed.

The versions I used to create this project are as follows:
- python 3.9.6
- node 18.15.0
- npm 9.5.0

You can check your versions by running these commands in your terminal
```bash
npm -v
node -v
python -V
```

I recommend creating a python virtual environment to manage the dependencies. You can create one with:

```
python -m venv <name of venv>
source <name of venv>/bin/activate
```
Once you've activated the virtual environment, you can install the python dependencies from the requirements.txt and JS dependencies from package.json. Run the following 2 commands in your terminal:

```
pip install -r requirements.txt
npm install
```

Next, we must populate the database. First, make sure there is a database file in the backend folder called database.db. If so, run this command to populate it:

```
python backend/data_upload.py
```

Now, you should be ready to run the project. Launch 2 terminals and in the first, start the flask app:

```
python backend/app.py
```

Then, start the React app by running this command in another terminal:

```
npm start
```

Congratulations, you have successfully started my Lion Auction app.



import React, {useState, useEffect, useContext} from 'react';
import './AuctionDetails.css'
import { Button, Dialog, DialogTitle, DialogContent, DialogContentText, TextField, DialogActions } from '@mui/material';
import { Snackbar } from '@mui/material';
import UserContext from "./UserContext";
import PaymentModal from './PaymentModal';
const AuctionDetails = ({ listingId , onBackButtonClick }) => {
  const [auctionDetails, setAuctionDetails] = useState(null);
  const [allBids, setAllBids] = useState([]);
  const [placeBidModalOpen, setPlaceBidModalOpen] = useState(false);
  const [newBidAmount, setNewBidAmount] = useState(0);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [paymentModalOpen, setPaymentModalOpen] = useState(false);
  const {userEmail} = useContext(UserContext);


  useEffect(() => {
    const fetchData = async () => {
        const [details, allBids] = await Promise.all([
          fetchAuctionDetails(listingId),
          fetchAllBids(listingId),
        ]);

    setAuctionDetails(details.listing);
    setAllBids(allBids.bids);
  };

  fetchData();
  }, [listingId]);

  const updateData = async () => {
    const [details, allBids] = await Promise.all([
      fetchAuctionDetails(listingId),
      fetchAllBids(listingId),
    ]);
    setAuctionDetails(details.listing);
    setAllBids(allBids.bids);
  }

  const fetchAllBids = async (listingId) => {
    const response = await fetch('http://127.0.0.1:5000/get_all_bids', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ Listing_ID: listingId }),
    });
    const data = await response.json();
    return data;
  };
  const fetchAuctionDetails = async (listingId) => {
    const response = await fetch('http://127.0.0.1:5000/get_auction_details', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ Listing_ID: listingId }),
    });
    const data = await response.json();
    return data;
  };

  const handleSubmitPayment = async (paymentDetails) => {
    const bidId = allBids[0].Bid_ID;

    const response = await fetch("http://127.0.0.1:5000/complete_transaction", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ bid_id: bidId }),
    });

    const data = await response.json();
    if (data.success) {

      setPaymentModalOpen(false);
      onBackButtonClick()
    } else {
      // Show the error message
      setSnackbarMessage(data.message);
      setSnackbarOpen(true);
    }

  };

  const handlePlaceBidClick = () => {
    setPlaceBidModalOpen(true);
  };

  const handleCloseBidModal = () => {
    setPlaceBidModalOpen(false);
  };

  const handlePlaceBid = async () => {

    const bidData = {
      Seller_Email: auctionDetails.Seller_Email,
      Listing_ID: listingId,
      Bidder_Email: userEmail,
      Bid_Price: parseFloat(newBidAmount),
    };

    const response = await fetch("http://127.0.0.1:5000/place_bid", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bidData),
    });

    const data = await response.json();
    if (data.success) {
      handleCloseBidModal();
      updateData()
      if (data.message === "Last Bid") {
        setPaymentModalOpen(true);
      }
    } else {
      // Show the error message
      setSnackbarMessage(data.message);
      setSnackbarOpen(true);
    }
  };
  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };


  if (!auctionDetails || !allBids) {
    return <div>Loading...</div>;
  }

  return (
    <div className="auction-details">

        <Dialog open={placeBidModalOpen} onClose={handleCloseBidModal}>
          <DialogTitle>Place a Bid</DialogTitle>
          <DialogContent>
            <DialogContentText>
              To place a bid, enter an amount at least $1 higher than the current highest bid.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="bid"
              label="Bid Amount"
              type="number"
              fullWidth
              variant="standard"
              value={newBidAmount}
              onChange={(e) => setNewBidAmount(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseBidModal}>Cancel</Button>
            <Button onClick={handlePlaceBid} color="primary">
              Place Bid
            </Button>
          </DialogActions>
        </Dialog>
      <PaymentModal
        open={paymentModalOpen}
        onClose={() => setPaymentModalOpen(false)}
        onSubmitPayment={handleSubmitPayment}
      />
      <div className="header">
        <button className="back-button" onClick={onBackButtonClick}>
          Back to Category Browsing
        </button>
        <h2>{auctionDetails.Auction_Title}</h2>
      </div>
      <p>Product Name: {auctionDetails.Product_Name}</p>
      <p>Description: {auctionDetails.Product_Description}</p>
      <p>Quantity: {auctionDetails.Quantity}</p>
      <p>Reserve Price: {auctionDetails.Reserve_Price}</p>
      <p>Remaining Bids: {auctionDetails.Max_bids - allBids.length}</p>
      <p>Seller: {auctionDetails.Seller_Email}</p>
      <Button classname="bid-button" variant="contained" color="primary" onClick={handlePlaceBidClick}>
          Place Bid
      </Button>

      <h3>Bids:</h3>
       {allBids.length > 0 ? (
        <table className="bids-table">
          <thead>
            <tr>
              <th>Bid ID</th>
              <th>Listing ID</th>
              <th>Bidder Email</th>
              <th>Bid Price</th>
            </tr>
          </thead>
          <tbody>
            {allBids.map((bid) => (
              <tr key={bid.Bid_ID}>
                <td>{bid.Bid_ID}</td>
                <td>{bid.Listing_ID}</td>
                <td>{bid.Bidder_Email}</td>
                <td>{bid.Bid_Price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No bids for this auction.</p>
      )}
      <Snackbar
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        open={snackbarOpen}
        onClose={handleCloseSnackbar}
        message={snackbarMessage}
        autoHideDuration={5000}
        key={"snackbar"}
      />
    </div>
  );
};

export default AuctionDetails;
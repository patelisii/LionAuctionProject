import React, { useState, useEffect, useContext } from 'react';
import UserContext from './UserContext';
import './SellerListings.css';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
const SellerListings = () => {
  const {userEmail} = useContext(UserContext);
  const [listings, setListings] = useState([]);
  const [showCreateListingModal, setShowCreateListingModal] = useState(false);

  const handleOpenCreateListingModal = () => {
    setShowCreateListingModal(true);
  };

  const handleCloseCreateListingModal = () => {
    setShowCreateListingModal(false);
  };


  useEffect(() => {
    // Fetch the listings for the current seller.
    fetchSellerListings(userEmail).then((data) => {
      setListings(data);
    });
  }, [userEmail]);

  const fetchSellerListings = async (sellerEmail) => {
    // Fetch the listings for the given seller from the Flask app
    const response = await fetch('http://127.0.0.1:5000/get_seller_listings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({email: sellerEmail}),
    });
    const data = await response.json();
    return data;
  };

  const [openModal, setOpenModal] = useState(false);
  const [selectedListing, setSelectedListing] = useState(null);

  const handleOpenModal = (listing) => {
    setSelectedListing(listing);
    setOpenModal(true);
  };


  const handleCloseModal = () => {
    setOpenModal(false);
  };

  return (
      <div className="seller-listings">
        <h2>Your Listings</h2>
        <button onClick={handleOpenCreateListingModal}>Create Listing</button>
        <table className="listings-table">
          <thead>
          <tr>
            <th>Auction Title</th>
            <th>Product Name</th>
            <th>Product Description</th>
            <th>Category</th>
            <th>Quantity</th>
            <th>Reserve Price</th>
            <th>Max Bids</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
          </thead>
          <tbody>
          {listings.map((listing) => (
              <tr key={listing.Listing_ID}>
                <td>{listing.Auction_Title}</td>
                <td>{listing.Product_Name}</td>
                <td>{listing.Product_Description}</td>
                <td>{listing.Category}</td>
                <td>{listing.Quantity}</td>
                <td>{listing.Reserve_Price}</td>
                <td>{listing.Max_bids}</td>
                <td>
                  {listing.Status === 0
                      ? 'Inactive'
                      : listing.Status === 2
                          ? 'Sold'
                          : 'Active'}
                </td>
                <td>
                  <button onClick={() => handleOpenModal(listing)}>Edit</button>
                </td>
              </tr>
          ))}
          </tbody>
        </table>
        {selectedListing && (
            <EditListingModal
                open={openModal}
                handleClose={handleCloseModal}
                listing={selectedListing}
                setListings={setListings}
                listings={listings}
            />
        )}
        <CreateListingModal
          open={showCreateListingModal}
          handleClose={handleCloseCreateListingModal}
          userEmail={userEmail}
          listings={listings}
          setListings={setListings}
        />
      </div>
  );
};

  const EditListingModal = ({ open, handleClose, listing, setListings, listings }) => {
    const [editedListing, setEditedListing] = useState(listing);

    useEffect(() => {
    setEditedListing(listing);
  }, [listing]);

    const handleChange = (e) => {
      setEditedListing({...editedListing, [e.target.name]: e.target.value});
    };

    const handleSave = async () => {
      // Update the listing in the backend
      const response = await fetch('http://127.0.0.1:5000/update_auction_listing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ listing_id: listing.Listing_ID, new_values: editedListing }),
      });

      if (response.ok) {
        // Update the listings state to reflect the changes
        const updatedListings = listings.map((l) => (l.Listing_ID === listing.Listing_ID ? editedListing : l));
        setListings(updatedListings);
        handleClose();
      } else {
        console.error('Failed to update listing');
      }
    };

    return (
        <Dialog open={open} onClose={handleClose}>
          <DialogTitle>Edit Auction Listing</DialogTitle>
          <DialogContent>
            <TextField label="Auction Title" fullWidth value={editedListing.Auction_Title} name="Auction_Title"
                       onChange={handleChange} margin="normal"/>
            <TextField label="Product Name" fullWidth value={editedListing.Product_Name} name="Product_Name"
                       onChange={handleChange} margin="normal"/>
            <TextField label="Product Description" fullWidth value={editedListing.Product_Description}
                       name="Product_Description" onChange={handleChange} margin="normal"/>

            <TextField label="Category" fullWidth value={editedListing.Category} name="Category" onChange={handleChange}
                       margin="normal"/>
            <TextField label="Quantity" fullWidth value={editedListing.Quantity} name="Quantity" type="number"
                       onChange={handleChange} margin="normal"/>
            <TextField label="Reserve Price" fullWidth value={editedListing.Reserve_Price} name="Reserve_Price"
                       onChange={handleChange} margin="normal"/>
            <TextField label="Max Bids" fullWidth value={editedListing.Max_bids} name="Max_bids" type="number"
                       onChange={handleChange} margin="normal"/>

            <FormControl fullWidth margin="normal">
              <InputLabel>Status</InputLabel>
              <Select value={editedListing.Status} name="Status" onChange={handleChange}>
                <MenuItem value={0}>Inactive</MenuItem>
                <MenuItem value={1}>Active</MenuItem>
                {/*<MenuItem value={2}>Sold</MenuItem>*/}
              </Select>
            </FormControl>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleSave} variant="contained">
              Save
            </Button>
          </DialogActions>
        </Dialog>
    );
  };

  const CreateListingModal = ({ open, handleClose, userEmail, listings, setListings }) => {
  const [newListing, setNewListing] = useState({
    Seller_Email: userEmail,
    Auction_Title: "",
    Product_Name: "",
    Product_Description: "",
    Category: "",
    Quantity: "",
    Reserve_Price: "",
    Max_bids: "",
    Status: "",
  });

  const handleChange = (e) => {
    setNewListing({ ...newListing, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const response = await fetch('http://127.0.0.1:5000/create_auction_listing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ listing: newListing }),
    });

    if (response.ok) {
      // Refresh the table if the creation is successful
      const { listing_id } = await response.json();
      const createdListing = { ...newListing, Listing_ID: listing_id };
      setListings([...listings, createdListing]);
      handleClose();
    } else {
      console.error('Failed to create listing');
    }
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>Create Auction Listing</DialogTitle>
      <DialogContent>
        <TextField label="Auction Title" fullWidth value={newListing.Auction_Title} name="Auction_Title" onChange={handleChange} margin="normal" />
        <TextField label="Product Name" fullWidth value={newListing.Product_Name} name="Product_Name" onChange={handleChange} margin="normal" />
        <TextField label="Product Description" fullWidth value={newListing.Product_Description} name="Product_Description" onChange={handleChange} margin="normal" />
        <TextField label="Category" fullWidth value={newListing.Category} name="Category" onChange={handleChange} margin="normal" />
        <TextField label="Quantity" fullWidth value={newListing.Quantity} name="Quantity" type="number" onChange={handleChange} margin="normal" />
        <TextField label="Reserve Price" fullWidth value={newListing.Reserve_Price} name="Reserve_Price" onChange={handleChange} margin="normal" />
        <TextField label="Max Bids" fullWidth value={newListing.Max_bids} name="Max_bids" type="number" onChange={handleChange} margin="normal" />
        <FormControl fullWidth margin="normal">
          <InputLabel>Status</InputLabel>
          <Select value={newListing.Status} name="Status" onChange={handleChange}>
            {/*<MenuItem value={0}>Inactive</MenuItem>*/}
            <MenuItem value={1}>Active</MenuItem>
            {/*<MenuItem value={2}>Sold</MenuItem>*/}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">Create</Button>
      </DialogActions>
    </Dialog>
  );
};

export default SellerListings;
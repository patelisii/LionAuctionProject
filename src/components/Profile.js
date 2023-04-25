import React, { useContext, useEffect, useState } from 'react';
import UserContext from './UserContext';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';

const ProfilePage = () => {
  const { userType, userEmail } = useContext(UserContext);
  const [userData, setUserData] = useState(null);
  const [showEditProfileModal, setShowEditProfileModal] = useState(false);
  const [editedUserData, setEditedUserData] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // API call to Flask backend
        const response = await fetch('http://127.0.0.1:5000/get_profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: userEmail, userType }), // Send email and userType as request body
        });
        const responseData = await response.json();
        setUserData(responseData);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, [userType, userEmail]);

  const handleUpdateProfile = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/update_profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: userEmail, userType, updatedData: editedUserData }),
        });

        if (response.ok) {
          setUserData(editedUserData);
          handleCloseEditProfileModal();
        } else {
          console.error('Failed to update user profile');
        }
      } catch (error) {
        console.error('Error updating user profile:', error);
      }
    };

  const handleOpenEditProfileModal = () => {
      setShowEditProfileModal(true);
      setEditedUserData(userData);
    };

  const handleCloseEditProfileModal = () => {
      setShowEditProfileModal(false);
    };

  const renderUserInfo = () => {
    if (!userData) return null;

    switch (userType) {
      case 'Bidder':
        return (
          <div>
            <p>email: {userData.email}</p>
            <p>Gender: {userData.gender}</p>
            <p>Age: {userData.age}</p>
            <p>Major: {userData.major}</p>
            <p>Address: {userData.address}</p>
            <p>Last 4 digits of Credit Card: {userData.cardDigits}</p>
          </div>
        );

      case 'Seller':
        return (
          <div>
            <p>email: {userData.email}</p>
            <p>Gender: {userData.gender}</p>
            <p>Age: {userData.age}</p>
            <p>Major: {userData.major}</p>
            <p>Address: {userData.address}</p>
            <p>Last 4 digits of Credit Card: {userData.cardDigits}</p>
            <p>Balance: {userData.balance}</p>
            <p>Bank Routing Number: {userData.bankRoutingNumber}</p>
            <p>Bank Account Number: {userData.bankAccountNumber}</p>
          </div>
        );

      case 'Local Business':
        return (
          <div>
            <p>Business Email: {userData.email}</p>
            <p>Business Address: {userData.address}</p>
            <p>Customer Service Phone Number: {userData.customerServiceNumber}</p>
            <p>Balance: {userData.balance}</p>
            <p>Bank Routing Number: {userData.bankRoutingNumber}</p>
            <p>Bank Account Number: {userData.bankAccountNumber}</p>
          </div>
        );
       case 'Helpdesk':
        return (
          <div>
            <p>email: {userData.email}</p>
            <p>position: {userData.position}</p>
            <p>Gender: {userData.gender && userData.gender}</p>
            <p>Age: {userData.age}</p>
            <p>Major: {userData.major}</p>
            <p>Address: {userData.address}</p>
            <p>Last 4 digits of Credit Card: {userData.cardDigits}</p>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div>
      <h1>
        {userData && userData.firstName} {userData && userData.lastName} {userData && userData.businessName} - {userType}
      </h1>
      {renderUserInfo()}
      {userType === "Bidder" && (
          <Button variant="contained" onClick={handleOpenEditProfileModal}>
            Edit Profile
          </Button>
      )}
        {editedUserData && (
          <Dialog open={showEditProfileModal} onClose={handleCloseEditProfileModal}>
            <DialogTitle>Edit Profile</DialogTitle>
            <DialogContent>
              <TextField
                label="First Name"
                fullWidth
                value={editedUserData.firstName || ""}
                onChange={(e) =>
                  setEditedUserData({ ...editedUserData, firstName: e.target.value })
                }
                margin="normal"
              />
              <TextField
                label="Last Name"
                fullWidth
                value={editedUserData.lastName || ""}
                onChange={(e) =>
                  setEditedUserData({ ...editedUserData, lastName: e.target.value })
                }
                margin="normal"
              />
              <TextField
                label="Gender"
                fullWidth
                value={editedUserData.gender || ""}
                onChange={(e) =>
                  setEditedUserData({ ...editedUserData, gender: e.target.value })
                }
                margin="normal"
              />
              <TextField
                label="Major"
                fullWidth
                value={editedUserData.major || ""}
                onChange={(e) =>
                  setEditedUserData({ ...editedUserData, major: e.target.value })
                }
                margin="normal"
              />

            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseEditProfileModal}>Cancel</Button>
              <Button onClick={handleUpdateProfile} variant="contained">
                Save
              </Button>
            </DialogActions>
          </Dialog>
        )}
      </div>

  );
};

export default ProfilePage;


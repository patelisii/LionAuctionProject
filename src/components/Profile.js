import React, { useContext, useEffect, useState } from 'react';
import UserContext from './UserContext';

const ProfilePage = () => {
  const { userType, userEmail } = useContext(UserContext);
  const [userData, setUserData] = useState(null);

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
    </div>
  );
};

export default ProfilePage;


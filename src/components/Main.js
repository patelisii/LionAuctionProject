import React, {useContext} from 'react';
import { useNavigate } from 'react-router-dom';
import UserContext from "./UserContext";
import CategoryView from './CategoryView';
import { Link } from 'react-router-dom';
import './Main.css'

const MainScreen = () => {
  const navigate = useNavigate();
  const { userType, userEmail } = useContext(UserContext);
  const fetchAuctionListings = async (categoryName) => {
    const response = await fetch('http://127.0.0.1:5000/get_products_by_category', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ category: categoryName }),
    });
    const data = await response.json();
    return data;
};

  const handleProfileClick = () => {
    navigate('/profile');
  };

  return (
    <div>
      {/* Navigation bar */}
      <nav className="navbar">
        <h1>LionAuction</h1>
        {["Seller", "Local Vendor"].includes(userType) && (
          <Link to="/seller-listings">
            <button className="seller-listings-btn">Seller Listings</button>
          </Link>
        )}
        <button onClick={handleProfileClick} className="profile-btn">Profile</button>
      </nav>

      <div className="App">
        <CategoryView fetchAuctionListings={fetchAuctionListings} />
      </div>
    </div>
  );
};

export default MainScreen;
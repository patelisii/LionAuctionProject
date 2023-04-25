import React, { useState, useEffect } from 'react';
import './CategoryView.css';
import AuctionDetails from './AuctionDetails';

const CategoryView = ({ fetchAuctionListings }) => {
  const [categories, setCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [auctionListings, setAuctionListings] = useState([]);
  const [parentCategory, setParentCategory] = useState(null);
  const [selectedListingId, setSelectedListingId] = useState(null);
  const [showAuctionDetails, setShowAuctionDetails] = useState(false);

  useEffect(() => {
    fetchTopLevelCategories().then((data) => {
      setCategories(data);
    });
  }, []);
  const fetchTopLevelCategories = async () => {
    const response = await fetch('http://127.0.0.1:5000/get_topLevel_categories');
    const data = await response.json();
    return data;
  };

  const fetchSubCategories = async (parentCategory) => {
    // Fetch subcategories for a given parent category
    const response = await fetch('http://127.0.0.1:5000/get_child_categories', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ category: parentCategory }),
    });
    const data = await response.json();
    return data;
  };

  const fetchParentCategory = async (categoryName) => {
    const response = await fetch('http://127.0.0.1:5000/get_parent_category', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ category: categoryName }),
    });
    const data = await response.json();
    return data.length ? data[0] : null;
  };

  const handleCategoryClick = async (categoryName) => {
    setActiveCategory(categoryName);
    const subCategories = await fetchSubCategories(categoryName);
    setCategories(subCategories);

    const fetchedAuctionListings = await fetchAuctionListings(categoryName);
    setAuctionListings(fetchedAuctionListings);

    const parent = await fetchParentCategory(categoryName);
    setParentCategory(parent);
  };

  const handleAuctionItemClick = (listingId) => {
    setSelectedListingId(listingId);
    setShowAuctionDetails(true);
  };
   const handleBackButtonClick = () => {
    setShowAuctionDetails(false);
    setSelectedListingId(null);
    handleCategoryClick(activeCategory)
  };


  return (
    <div className="category-view">
      {showAuctionDetails ? (
        <AuctionDetails listingId={selectedListingId} onBackButtonClick={handleBackButtonClick} />
      ) : (
        <>
          <div className="categories-section">
            <h2>{activeCategory === "Root" ? "Categories" : activeCategory}</h2>
            {parentCategory && (
              <button
                className="back-to-parent"
                onClick={() => handleCategoryClick(parentCategory)}
              >
                Back to {parentCategory}
              </button>
            )}
            <ul className="categories">
              {categories.map((categoryName) => (
                <li key={categoryName} onClick={() => handleCategoryClick(categoryName)}>
                  {categoryName}
                </li>
              ))}
            </ul>
          </div>
          <div className="auction-listings-section">
            <h2 align={"left"}>Auction Listings</h2>
            <ul className="auction-listings">
              {auctionListings.map((listing) => (
                <li key={listing.Listing_ID} onClick={() => handleAuctionItemClick(listing.Listing_ID)}>
                  <h3>{listing.Auction_Title}</h3>
                  <p>{listing.Product_Name}</p>
                  <p>{listing.Product_Description}</p>
                  <p>{listing.Seller_Email}</p>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
};

export default CategoryView;
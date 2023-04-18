import React, { useState, useEffect } from 'react';
import './CategoryView.css';

const CategoryView = ({ fetchAuctionListings }) => {
  const [categories, setCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [auctionListings, setAuctionListings] = useState([]);

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

  const handleCategoryClick = async (categoryName) => {
    setActiveCategory(categoryName);
    const subCategories = await fetchSubCategories(categoryName);
    setCategories(subCategories);

    const fetchedAuctionListings = await fetchAuctionListings(categoryName);
    setAuctionListings(fetchedAuctionListings);
  };

  return (
    <div className="category-view">
      <h2>Categories</h2>
      <ul className="categories">
        {categories.map((categoryName) => (
          <li key={categoryName} onClick={() => handleCategoryClick(categoryName)}>
            {categoryName}
          </li>
        ))}
      </ul>
      &nbsp;
      <h2>Auction Listings</h2>
      <ul className="auction-listings">
        {auctionListings.map((listing) => (
          <li key={listing.Listing_ID}>
            <h3>{listing.Auction_Title}</h3>
            <p>{listing.Product_Name}</p>
            <p>{listing.Product_Description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CategoryView;
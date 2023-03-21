import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const goToLoginPage = () => {
    navigate('/login');
  };

  return (
    <div>
      <h1>Welcome to LionAuction!</h1>
      <button onClick={goToLoginPage}>Login</button>
    </div>
  );
};

export default HomePage;
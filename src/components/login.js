import React, { useState, useContext } from 'react';
import {Button} from './button'
import {useNavigate} from "react-router-dom";
import UserContext from './UserContext';
const LoginPage = () =>{
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const { userType, setUserType, setUserEmail } = useContext(UserContext);

  const goToMainPage = () => {
    navigate('/main');
  };
  const handleLogin = async () => {
    // Clear the message
    setMessage('');


    try {
        // Make API call to Flask backend
        const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, userType }),
        });

        // Parse JSON data from the response
        const responseData = await response.json();

        // set the message received from Flask API call
        setMessage(responseData.message)
        if (responseData.message==="Login successful"){
            setUserEmail(email);
            goToMainPage()
        }


    } catch (error) {
      setMessage('An error occurred while logging in. Please try again later.');
    }
  };
   return (
    <div className="App">
      <h1>LionAuction Login &nbsp;</h1>
      <div>
        <label htmlFor="email" className="text-gray-600 font-semibold">Email:</label>
        <input
          type="text"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div>
        &nbsp;
      </div>
      <div>
        <label htmlFor="password" className="text-gray-600 font-semibold">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
        <div>
        &nbsp;
      </div>
      <div>
        <label htmlFor="userType" className="text-gray-600 font-semibold">
          User Type:
        </label>
        <select
          id="userType"
          value={userType}
          onChange={(e) => setUserType(e.target.value)}
        >
          <option value="Bidder">Bidder</option>
          <option value="Seller">Seller</option>
          <option value="Local Business">Local Business</option>
          <option value="Helpdesk">Helpdesk</option>
        </select>
      </div>
        <div>
        &nbsp;
      </div>
      <Button onClick={handleLogin}>Login</Button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default LoginPage;

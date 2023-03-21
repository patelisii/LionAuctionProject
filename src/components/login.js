import React, { useState } from 'react';
import {Button} from './button'
const LoginPage = () =>{
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    // Clear the message
    setMessage('');

    try {
      // Make API call to your Flask backend
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      // Parse JSON data from the response
      const responseData = await response.json();

      setMessage(responseData.message)

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
      <Button onClick={handleLogin}>Login</Button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default LoginPage;

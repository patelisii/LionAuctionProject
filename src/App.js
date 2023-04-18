import React, { useState }  from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/home';
import LoginPage from './components/login';
import './App.css';
import MainScreen from "./components/Main";
import UserContext from './components/UserContext';
import Profile from "./components/Profile";

function App() {
    const [userEmail, setUserEmail] = useState('');
    const [userType, setUserType] = useState('Bidder');
    return (
    <Router>
        <UserContext.Provider value={{ userType, setUserType, userEmail, setUserEmail}}>
            <div className="App">
                <Routes>
                    <Route path="/" exact element={<HomePage/>} />
                    <Route path="/login" element={<LoginPage/>} />
                    <Route path="/main" element={<MainScreen/>} />
                    <Route path="/profile" element={<Profile/>} />
                </Routes>
            </div>
        </UserContext.Provider>
    </Router>
    );
}

export default App;
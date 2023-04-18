import { createContext } from 'react';

const UserContext = createContext({
  userType: 'bidder',
  setUserType: () => {},
  userEmail:'None',
  setUserEmail: () => {}
});

export default UserContext;
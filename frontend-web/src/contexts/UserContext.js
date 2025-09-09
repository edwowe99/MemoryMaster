import React, { createContext, useState, useEffect } from 'react';

export const UserContext = createContext(null);

export function UserProvider({ children }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Simulate a logged-in user
        setUser({
            id: 1,
            username: "epowe",
            email: "edwar_owens@hotmail.co.uk",
        });
    }, []);

  return (
    <UserContext.Provider value={{ user }}>
      {children}
    </UserContext.Provider>
  );
}
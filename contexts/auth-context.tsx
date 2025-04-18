"use client";

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

interface AuthContextType {
  token: string | null;
  username: string | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

interface DecodedToken {
  username: string;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  username: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: false
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        try {
          const decoded = jwtDecode<DecodedToken>(storedToken);
          setToken(storedToken);
          setUsername(decoded.username);
        } catch (error) {
          console.error("Failed to decode token from storage:", error);
          localStorage.removeItem('auth_token');
        }
      }
    }
  }, []);

  const login = (newToken: string) => {
    try {
      const decoded = jwtDecode<DecodedToken>(newToken);
      localStorage.setItem('auth_token', newToken);
      setToken(newToken);
      setUsername(decoded.username);
    } catch (error) {
      console.error("Failed to decode new token:", error);
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setToken(null);
    setUsername(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{
      token,
      username,
      login,
      logout,
      isAuthenticated: !!token
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext); 
"use client";

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

interface AuthContextType {
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: false
});

export function AuthProvider({ children }: { children: ReactNode }) {
  // Initialize token state from localStorage
  const [token, setToken] = useState<string | null>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  });

  // Effect to sync token with localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken !== token) {
        console.log('Syncing token from localStorage:', storedToken);
        setToken(storedToken);
      }
    }
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem('auth_token', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setToken(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{
      token,
      login,
      logout,
      isAuthenticated: !!token
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext); 
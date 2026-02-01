import React, { createContext, useState, useEffect, ReactNode } from 'react';
// import { supabase } from '../lib/supabase'; // Removed Supabase import
// import { User, Session } from '@supabase/supabase-js'; // Removed Supabase types
import axios from 'axios';

interface AccountInfo {
  uqid: number;
  uid: string;
  uemail: string;
  level: 'admin' | 'manager' | 'viewer';
  status: string;
}

interface Permissions {
  can_create: boolean;
  can_edit: boolean;
  can_delete: boolean;
  can_view: boolean;
}

// New interface for JWT based auth session
interface JWTSession {
  access_token: string;
  // Add other relevant session info if provided by backend, e.g., expiry
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: AccountInfo | null; // User will now be the AccountInfo
  session: JWTSession | null; // Session will be a simpler object with the JWT
  account: AccountInfo | null;
  level: 'admin' | 'manager' | 'viewer' | null;
  permissions: Permissions | null;
  login: (email: string, password: string) => Promise<{ error?: string }>;
  signup: (email: string, password: string) => Promise<{ error?: string }>; // Keeping for now, can be removed if not needed
  logout: () => Promise<void>;
  refreshAccountInfo: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<AccountInfo | null>(null); // Changed type
  const [session, setSession] = useState<JWTSession | null>(null); // Changed type
  const [account, setAccount] = useState<AccountInfo | null>(null);
  const [level, setLevel] = useState<'admin' | 'manager' | 'viewer' | null>(null);
  const [permissions, setPermissions] = useState<Permissions | null>(null);

  const fetchAccountInfo = async (token: string) => { // Accepts token string directly
    console.log('AuthContext: fetchAccountInfo received token:', token ? token.substring(0, 30) + '...' : 'None');
    if (!token) {
      setAccount(null);
      setLevel(null);
      setPermissions(null);
      return;
    }

    try {
      const response = await axios.post(
        '/api/auth/verify',
        { token: token }, // Pass token directly
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.data.authenticated && response.data.account) {
        setAccount(response.data.account);
        setLevel(response.data.level);
        setPermissions(response.data.permissions);
        setUser(response.data.account); // Set user as account info
      } else {
        setAccount(null);
        setLevel(null);
        setPermissions(null);
        setUser(null);
      }
      setIsAuthenticated(response.data.authenticated); // Update isAuthenticated based on backend
    } catch (error) {
      console.error('Failed to fetch account info:', error);
      setAccount(null);
      setLevel(null);
      setPermissions(null);
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('jwt_access_token');
      console.log('AuthContext: Retrieved storedToken from localStorage:', storedToken ? storedToken.substring(0, 30) + '...' : 'None');
      if (storedToken) {
        setSession({ access_token: storedToken });
        console.log('AuthContext: Calling fetchAccountInfo with stored token.');
        await fetchAccountInfo(storedToken);
      } else {
        console.log('AuthContext: No stored token found in localStorage.');
        setIsAuthenticated(false);
        setUser(null);
        setSession(null);
        setAccount(null);
        setLevel(null);
        setPermissions(null);
      }
    };

    initializeAuth();
  }, []); // Run only once on mount

    const login = async (email: string, password: string) => {
      try {
        const response = await axios.post('/api/auth/login', { email, password });
        const { access_token, user: accountData, level: userLevel } = response.data;
  
        localStorage.setItem('jwt_access_token', access_token);
        console.log('AuthContext: Stored access_token in localStorage:', access_token ? access_token.substring(0, 30) + '...' : 'None');
        setSession({ access_token });
        setUser(accountData);
        setAccount(accountData);
        setLevel(userLevel);
        setIsAuthenticated(true);
        await fetchAccountInfo(access_token); // Fetch detailed account info and permissions
        return {}; // No error
      } catch (err: any) {
        console.error('Login failed:', err);
        return { error: err.response?.data?.error || '로그인 실패' };
      }
    };
  
  const signup = async (_email: string, _password: string) => {
    // Implement internal signup if needed, for now just a placeholder
    // For now, no direct signup via frontend for internal users.
    // Accounts are to be created by admins/managers.
    return { error: '회원가입은 관리자를 통해서만 가능합니다.' };
  };
  
    const logout = async () => {
      localStorage.removeItem('jwt_access_token');
      console.log('AuthContext: Cleared access_token from localStorage.');
      setIsAuthenticated(false);
      setUser(null);
      setSession(null);
      setAccount(null);
      setLevel(null);
      setPermissions(null);
    };
  
    const refreshAccountInfo = async () => {
      if (session?.access_token) {
        console.log('AuthContext: Refreshing account info with token.');
        await fetchAccountInfo(session.access_token);
      }
    };
  
    return (
      <AuthContext.Provider value={{
        isAuthenticated,
        user,
        session,
        account,
        level,
        permissions,
        login,
        signup,
        logout,
        refreshAccountInfo
      }}>
        {children}
      </AuthContext.Provider>
    );
  };
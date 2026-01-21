import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { supabase } from '../lib/supabase';
import { User, Session } from '@supabase/supabase-js';
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

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  session: Session | null;
  account: AccountInfo | null;
  level: 'admin' | 'manager' | 'viewer' | null;
  permissions: Permissions | null;
  login: (email: string, password: string) => Promise<{ error: any }>;
  signup: (email: string, password: string) => Promise<{ error: any }>;
  logout: () => Promise<void>;
  refreshAccountInfo: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [account, setAccount] = useState<AccountInfo | null>(null);
  const [level, setLevel] = useState<'admin' | 'manager' | 'viewer' | null>(null);
  const [permissions, setPermissions] = useState<Permissions | null>(null);

  const fetchAccountInfo = async (session: Session | null) => {
    if (!session?.access_token) {
      setAccount(null);
      setLevel(null);
      setPermissions(null);
      return;
    }

    try {
      const response = await axios.post(
        '/api/auth/verify',
        { token: session.access_token },
        {
          headers: {
            'Authorization': `Bearer ${session.access_token}`
          }
        }
      );

      if (response.data.authenticated && response.data.account) {
        setAccount(response.data.account);
        setLevel(response.data.level);
        setPermissions(response.data.permissions);
      } else {
        setAccount(null);
        setLevel(null);
        setPermissions(null);
      }
    } catch (error) {
      console.error('Failed to fetch account info:', error);
      setAccount(null);
      setLevel(null);
      setPermissions(null);
    }
  };

  useEffect(() => {
    // Check current session
    supabase.auth.getSession().then(async ({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setIsAuthenticated(!!session);
      if (session) {
        await fetchAccountInfo(session);
      }
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
      setIsAuthenticated(!!session);
      if (session) {
        await fetchAccountInfo(session);
      } else {
        setAccount(null);
        setLevel(null);
        setPermissions(null);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const login = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    return { error };
  };

  const signup = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
    });
    return { error };
  };

  const logout = async () => {
    await supabase.auth.signOut();
    setAccount(null);
    setLevel(null);
    setPermissions(null);
  };

  const refreshAccountInfo = async () => {
    if (session) {
      await fetchAccountInfo(session);
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
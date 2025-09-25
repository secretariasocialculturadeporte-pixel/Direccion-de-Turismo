"use client";

import React, { createContext, useState, useContext, useEffect, ReactNode, useCallback } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const API_BASE_URL = 'http://localhost:8000/api';

interface User {
  pk: number;
  username: string;
  email: string;
  role: 'ADMIN' | 'FUNCIONARIO' | 'PRESTADOR' | 'TURISTA';
}

interface SavedItem {
  id: number;
  object_id: number;
  content_type_name: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  mfaRequired: boolean;
  login: (email: string, password: string) => Promise<void>;
  verifyMfa: (code: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  // "Mi Viaje" related
  isItemSaved: (contentType: string, objectId: number) => boolean;
  toggleSaveItem: (contentType: string, objectId: number) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [loginCredentials, setLoginCredentials] = useState<{ email: string; password?: string; code?: string } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [savedItemsMap, setSavedItemsMap] = useState<Map<string, number>>(new Map());
  const router = useRouter();

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    setMfaRequired(false);
    setLoginCredentials(null);
    setSavedItemsMap(new Map());
    localStorage.removeItem('authToken');
    delete axios.defaults.headers.common['Authorization'];
    router.push('/');
  }, [router]);

  const fetchUserData = useCallback(async (authToken: string) => {
    try {
      const headers = { Authorization: `Token ${authToken}` };
      const userResponse = await axios.get(`${API_BASE_URL}/auth/user/`, { headers });
      setUser(userResponse.data);

      if (userResponse.data.role === 'TURISTA') {
        const savedItemsResponse = await axios.get(`${API_BASE_URL}/mi-viaje/`, { headers });
        const itemMap: Map<string, number> = new Map(savedItemsResponse.data.map((item: SavedItem) => [`${item.content_type_name}_${item.object_id}`, item.id]));
        setSavedItemsMap(itemMap);
      }
    } catch (error) {
      console.error("Error fetching user data, logging out:", error);
      logout();
    }
  }, [logout]);

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setToken(storedToken);
      axios.defaults.headers.common['Authorization'] = `Token ${storedToken}`;
      fetchUserData(storedToken).finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [fetchUserData]);

  const completeLogin = async (key: string) => {
    setToken(key);
    localStorage.setItem('authToken', key);
    axios.defaults.headers.common['Authorization'] = `Token ${key}`;
    setMfaRequired(false);
    setLoginCredentials(null);

    const userResponse = await axios.get(`${API_BASE_URL}/auth/user/`, { headers: { Authorization: `Token ${key}` } });
    const userData: User = userResponse.data;
    setUser(userData);

    if (userData.role === 'TURISTA') {
      await fetchUserData(key);
      router.push('/mi-viaje');
    } else {
      router.push('/dashboard');
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login/`, { email, password });
      if (response.data.key) {
        await completeLogin(response.data.key);
      } else {
        setMfaRequired(true);
        setLoginCredentials({ email, password });
      }
    } catch (error) {
      alert('Correo electrónico o contraseña incorrectos.');
      throw error;
    }
  };

  const verifyMfa = async (code: string) => {
    if (!loginCredentials) return;
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login/`, { ...loginCredentials, code });
      if (response.data.key) {
        await completeLogin(response.data.key);
      } else {
        alert('El código de verificación es incorrecto.');
      }
    } catch (error) {
      alert('Error al verificar el código. Inténtelo de nuevo.');
      throw error;
    }
  };

  const isItemSaved = (contentType: string, objectId: number): boolean => {
    return savedItemsMap.has(`${contentType}_${objectId}`);
  };

  const toggleSaveItem = async (contentType: string, objectId: number) => {
    if (!user || user.role !== 'TURISTA') {
      alert("Necesitas iniciar sesión como turista para guardar favoritos.");
      router.push('/login');
      return;
    }

    const itemKey = `${contentType}_${objectId}`;
    const savedItemId = savedItemsMap.get(itemKey);

    try {
      if (savedItemId) {
        await axios.delete(`${API_BASE_URL}/mi-viaje/${savedItemId}/`);
      } else {
        await axios.post(`${API_BASE_URL}/mi-viaje/`, { content_type: contentType, object_id: objectId });
      }
      // Refetch all items to ensure sync
      await fetchUserData(token!);
    } catch(error) {
      console.error("Error al guardar/eliminar el elemento:", error);
      alert("Hubo un error al procesar tu solicitud.");
    }
  };

  const value = {
    isAuthenticated: !!token,
    user,
    token,
    mfaRequired,
    login,
    verifyMfa,
    logout,
    isLoading,
    isItemSaved,
    toggleSaveItem,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};
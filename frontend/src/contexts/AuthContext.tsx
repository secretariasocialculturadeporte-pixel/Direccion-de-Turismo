"use client";

import React, { createContext, useState, useContext, useEffect, ReactNode, useCallback } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const API_URL = 'http://localhost:8000/api/auth/';

interface LoginCredentials {
  email: string;
  password?: string; // Password is not always needed
  code?: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  mfaRequired: boolean;
  login: (email: string, password: string) => Promise<void>;
  verifyMfa: (code: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [loginCredentials, setLoginCredentials] = useState<LoginCredentials | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setToken(storedToken);
      axios.defaults.headers.common['Authorization'] = `Token ${storedToken}`;
    }
    setIsLoading(false);
  }, []);

  const completeLogin = (key: string) => {
    setToken(key);
    localStorage.setItem('authToken', key);
    axios.defaults.headers.common['Authorization'] = `Token ${key}`;
    setMfaRequired(false);
    setLoginCredentials(null);
    router.push('/dashboard');
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post(`${API_URL}login/`, { email, password });

      // Si la respuesta tiene 'key', el login fue directo (sin 2FA)
      if (response.data.key) {
        completeLogin(response.data.key);
      } else {
        // Si no hay 'key', es que se necesita 2FA
        setMfaRequired(true);
        setLoginCredentials({ email, password });
      }
    } catch (error) {
      console.error('Error en el primer paso del login:', error);
      alert('Correo electrónico o contraseña incorrectos.');
      throw error;
    }
  };

  const verifyMfa = async (code: string) => {
    if (!loginCredentials) {
      alert("Error: No se encontraron las credenciales para la verificación.");
      return;
    }

    try {
      // Reenviamos las credenciales junto con el código 2FA
      const response = await axios.post(`${API_URL}login/`, {
        ...loginCredentials,
        code,
      });

      if (response.data.key) {
        completeLogin(response.data.key);
      } else {
        // Esto puede ocurrir si el código es incorrecto
        alert('El código de verificación es incorrecto.');
      }
    } catch (error) {
      console.error('Error al verificar el código 2FA:', error);
      alert('Error al verificar el código. Inténtelo de nuevo.');
      throw error;
    }
  };

  const logout = useCallback(() => {
    setToken(null);
    setMfaRequired(false);
    setLoginCredentials(null);
    localStorage.removeItem('authToken');
    delete axios.defaults.headers.common['Authorization'];
    router.push('/login');
  }, [router]);

  const value = {
    isAuthenticated: !!token,
    token,
    mfaRequired,
    login,
    verifyMfa,
    logout,
    isLoading,
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
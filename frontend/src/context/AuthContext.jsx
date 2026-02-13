import { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (token && storedUser && storedUser !== "undefined") {
      try {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        setUser(JSON.parse(storedUser));
        const res = await api.get('/auth/me');
        setUser(res.data);
      } catch (error) {
        console.error("Auth initialization failed:", error);
        logout(); 
      }
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = (token, userData) => {
    setUser(userData);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    console.log("AuthContext: Login function completed for", userData.full_name);
    navigate('/dashboard');
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
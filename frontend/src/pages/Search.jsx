import React, { useState, useEffect } from 'react';
import { Container, Toast, ToastContainer, Spinner, Alert } from 'react-bootstrap';
import api from '../services/api';
import SearchForm from '../components/SearchForm';
import Results from './Results';
import { useNavigate } from 'react-router-dom';


const Search = () => {
  const navigate = useNavigate();
  const [userPreferences, setUserPreferences] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");

  useEffect(() => {
    const fetchSavedPreferences = async () => {
      try {
        // Fetch the user's current profile which contains the preferences object
        const response = await api.get('/auth/me');
        if (response.data && response.data.preferences) {
          setUserPreferences(response.data.preferences);
        }
      } catch (err) {
        console.error("Failed to load preferences:", err);
        setError("Could not load your saved filters.");
      } finally {
        setLoading(false);
      }
    };

    fetchSavedPreferences();
  }, []);

  const handlePreferenceUpdate = async (formData) => {
    try {
      await api.put('/auth/preferences', formData);
      setToastMessage("Preferences saved successfully!");
      setShowToast(true);
      console.log("Searching with:", formData);
      navigate('/jobs/search', { state: { filters: formData } });
    } catch (error) {
      console.error("Update failed:", error);
      alert("Failed to save preferences.");
    }
  };

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">Loading your search criteria...</p>
      </Container>
    );
  }

  return (
    <Container className='mx-auto m-5'>
      <ToastContainer position="top-end" className="p-3" style={{ zIndex: 11 }}>
        <Toast
          onClose={() => setShowToast(false)}
          show={showToast}
          delay={3000}
          autohide
          bg="success"
        >
          <Toast.Header>
            <strong className="me-auto">System Update</strong>
            <small>Just now</small>
          </Toast.Header>
          <Toast.Body className="text-white">
            {toastMessage}
          </Toast.Body>
        </Toast>
      </ToastContainer>
      <h2 className="fw-bold mb-4">Job Search</h2>
      {error && <Alert variant="warning">{error}</Alert>}
      <SearchForm
        onSearch={handlePreferenceUpdate}
        initialData={userPreferences}
      />
    </Container>
  );
}
export default Search
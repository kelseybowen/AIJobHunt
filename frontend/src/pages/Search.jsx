import React, { useState, useEffect } from 'react';
import { Container, Toast, ToastContainer, Spinner, Alert } from 'react-bootstrap';
import api from '../services/api';
import Results from './Results';
import PreferencesSummary from '../components/PreferencesSummary';
import SearchForm from '../components/SearchForm';


const Search = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [userPreferences, setUserPreferences] = useState(null);
  const [loading, setLoading] = useState(true);
  const [prefsError, setPrefsError] = useState("");
  const [searchError, setSearchError] = useState("");
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    const fetchAndSearch = async () => {
      try {
        setLoading(true);
        const response = await api.get('/auth/me');
        if (response.data && response.data.preferences) {
          const prefs = response.data.preferences;
          setUserPreferences(prefs);
          // Search only runs if user has minimum of 1 skill and 1 target role
          const hasCriteria = prefs.skills?.length > 0 || prefs.target_roles?.length > 0;
          if (hasCriteria) {
            await handleSearch(prefs);
          }
        }
      } catch (err) {
        console.error("Initialization error:", err);
        setPrefsError("Could not load your saved preferences.");
      } finally {
        setLoading(false);
      }
    };
    fetchAndSearch();
  }, []);

  const handlePreferenceUpdate = async (formData) => {
    try {
      await api.put('/auth/preferences', formData);
      setToastMessage("Preferences saved successfully!");
      setShowToast(true);
      setIsEditing(false);
      await handleSearch(formData)
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to save preferences.");
    }
  };

  const handleSearch = async (criteria) => {
    setSearching(true);
    setSearchError("");
    try {
      const response = await api.post('/jobs/search', criteria);
      setResults(response.data);
    } catch (err) {
      console.error("Search API Error:", err);
      const message = err.response?.data?.detail || "Failed to fetch job matches. Please try again.";
      setSearchError(message);
    } finally {
      setSearching(false);
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
        <Toast onClose={() => setShowToast(false)} show={showToast} delay={3000} autohide bg="success">
          <Toast.Header><strong className="me-auto">System Update</strong></Toast.Header>
          <Toast.Body className="text-white">{toastMessage}</Toast.Body>
        </Toast>
      </ToastContainer>
      <h2 className="fw-bold mb-4">Job Search</h2>

      {(searchError || prefsError) && (
        <Alert variant="danger">
          {prefsError && <div>{prefsError}</div>}
          {searchError && <div>{searchError}</div>}
        </Alert>
      )}

      {isEditing ? (
        <SearchForm 
          initialData={userPreferences} 
          onSearch={handlePreferenceUpdate} 
          onCancel={() => setIsEditing(false)} 
        />
      ) : (
        <PreferencesSummary 
          preferences={userPreferences} 
          onEdit={() => setIsEditing(true)} 
        />
      )}

      <hr className="my-5" />

      {/* Search  Results*/}
      <div className="results-section">
        <h3 className="mb-4">AI-Matched Results</h3>
        
        {searching ? (
          <div className="text-center py-5">
            <Spinner animation="grow" variant="primary" />
            <p className="text-muted mt-2">Searching for matches...</p>
          </div>
        ) : (
          <Results results={results} /> 
        )}
      </div>
    </Container>
  );
}
export default Search
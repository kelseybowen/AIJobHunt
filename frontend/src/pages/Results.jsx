import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Container, Alert, Button, Spinner } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import JobCard from '../components/JobCard';
import api from '../services/api';

const Results = ({ results }) => {
  const location = useLocation();
  const { user, loading: authLoading } = useAuth();
  const [savedJobIds, setSavedJobIds] = useState(new Set());
  const filters = location.state?.filters;

  useEffect(() => {
    const fetchSavedJobs = async () => {
      const userId = user?.id || user?._id; 
      if (!userId) return;

      try {
        const response = await api.get(`/interactions/user/${userId}`);
        if (response.status === 200) {
          const interactions = response.data;
          const savedIds = new Set(
            interactions
              .filter(i => i.interaction_type === 'saved')
              .map(i => i.job_id)
          );
          setSavedJobIds(savedIds);
        }
      } catch (error) {
        console.error("Error loading saved jobs:", error);
      }
    };

    fetchSavedJobs();
  }, [user]);

  if (authLoading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2 text-muted">Loading your profile...</p>
      </Container>
    );
  }

  if (!results || results.length === 0) {
    return (
      <div className="text-center my-5">
        <p className="text-muted">No matches found in your preferred locations. Try adjusting your preferences.</p>
        <Button as={Link} to="/dashboard" variant="outline-primary">
          Edit Preferences
        </Button>
      </div>
    );
  }

  const formatCurrency = (value) => {
    return value ? Number(value).toLocaleString() : '0';
  };

  return (
    <Container className="mt-2 text-center">
      <h2 className="fw-bold my-3">Matching Jobs ({results.length})</h2>

      {filters && (
        <Alert variant="info" className="text-start d-inline-block shadow-sm mb-4">
          <div className="small">
            <strong>Target Roles:</strong> {filters.target_roles?.join(', ') || 'Any'} <br />
            <strong>Key Skills:</strong> {filters.skills?.join(', ') || 'Any'} <br />
            <strong>Locations:</strong> {filters.desired_locations?.length > 0 ? filters.desired_locations.join(', ') : 'Anywhere'} <br />
            <strong>Min Salary:</strong> ${formatCurrency(filters.salary_min)}
          </div>
        </Alert>
      )}

      <div className="job-list d-flex flex-column align-items-center gap-3">
        {results.map((job) => (
          <JobCard
            key={job.job_id || job._id || job.external_id}
            job={job}
            initialSaved={savedJobIds.has(job.job_id || job._id || job.id)}
            onUnsave={() => {
              const newSet = new Set(savedJobIds);
              newSet.delete(job.job_id || job._id || job.id);
              setSavedJobIds(newSet);
            }}
          />
        ))}
      </div>
    </Container>
  );
};

export default Results;
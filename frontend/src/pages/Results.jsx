import { useLocation, Link } from 'react-router-dom';
import { Container, Alert, Button } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import JobCard from '../components/JobCard';

const Results = ({ results }) => {
  const location = useLocation();
  const { user, loading } = useAuth();
  const [savedJobIds, setSavedJobIds] = useState(new Set());
  const filters = location.state?.filters;
  const fetch_url = import.meta.env.VITE_API_URL;

  // Get saved jobs to display saved status on JobCard
  useEffect(() => {
    const fetchSavedJobs = async () => {
      if (!user?.id) return;

      try {
        const response = await fetch(`${fetch_url}/interactions/user/${user.id}`);
        if (response.ok) {
          const interactions = await response.json();
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

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2 text-muted">Loading your profile...</p>
      </Container>
    );
  }

  if (!results || results.length === 0) {
    return <div className="text-center">
      <p className="text-center text-muted">No matches found. Try adjusting your skills.</p>
      <Button as={Link} to="/dashboard" variant="outline-secondary">
        Edit Preferences
      </Button>
    </div>
  }

  const formatCurrency = (value) => {
    return value ? value.toLocaleString() : '0';
  };

  return (
    <Container className="mt-2 text-center">
      <h2 className="fw-bold my-3">Matching Jobs ({results.length})</h2>

      {filters && (
        <Alert variant="info" className="text-start d-inline-block shadow-sm">
          <strong>Searching for:</strong> {filters.target_roles.join(', ')} <br />
          <strong>Skills:</strong> {filters.skills.join(', ')} <br />
          <strong>Location:</strong> {filters.desired_locations.join(', ') || 'Anywhere'} <br />
          <strong>Salary Range:</strong> ${formatCurrency(filters.salary_min)} — ${formatCurrency(filters.salary_max)}
        </Alert>
      )}

      <div className="job-list">
        {results.map((job) => (
          <JobCard
            key={job.external_id}
            job={job}
            initialSaved={savedJobIds.has(job.id || job._id)}
            onUnsave={() => setSavedJobs(prev => prev.filter(j => j.id !== job.id))}
          />
        ))}
      </div>

    </Container>
  );
};

export default Results;
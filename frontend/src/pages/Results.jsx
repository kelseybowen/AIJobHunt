import PageHeader from "../components/PageHeader"
import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Container, Alert, Button, Spinner } from 'react-bootstrap';
import JobCard from '../components/JobCard';

const Results = ({ results }) => {
  const location = useLocation();
  const filters = location.state?.filters;

  if (!results || results.length === 0) {
    return <p className="text-center text-muted">No matches found. Try adjusting your skills.</p>;
  }

  const formatCurrency = (value) => {
    return value ? value.toLocaleString() : '0';
  };

  return (
    <Container className="mt-5 text-center">
      <h2 className="fw-bold mb-3">Matching Jobs</h2>

      {filters ? (
        <Alert variant="info" className="text-start d-inline-block shadow-sm">
          <strong>Searching for:</strong> {filters.target_roles.join(', ')} <br />
          <strong>Skills:</strong> {filters.skills.join(', ')} <br />
          <strong>Location:</strong> {filters.desired_locations.join(', ') || 'Anywhere'} <br />
          <strong>Salary Range:</strong> ${formatCurrency(filters.salary_min)} — ${formatCurrency(filters.salary_max)}
        </Alert>
      ) : null}

      <div className="py-5">
        <Spinner animation="border" variant="primary" className="mb-3" role="status" />
        <p className="text-muted">
          Analyzing your search criteria to find your best match...
        </p>
        <Alert variant="warning" className="mt-4">
          <strong>Integration in progress:</strong> The Job Board API is being connected. Check back soon!
        </Alert>
      </div>

      <div className="job-list">
        {results.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>

      <Button as={Link} to="/dashboard" variant="outline-secondary">
        Edit Preferences
      </Button>
    </Container>
  );
};

export default Results;
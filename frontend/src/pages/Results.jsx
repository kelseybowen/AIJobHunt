import { useLocation, Link } from 'react-router-dom';
import { Container, Alert, Button } from 'react-bootstrap';
import JobCard from '../components/JobCard';

const Results = ({ results }) => {
  const location = useLocation();
  const filters = location.state?.filters;

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

      {filters ? (
        <Alert variant="info" className="text-start d-inline-block shadow-sm">
          <strong>Searching for:</strong> {filters.target_roles.join(', ')} <br />
          <strong>Skills:</strong> {filters.skills.join(', ')} <br />
          <strong>Location:</strong> {filters.desired_locations.join(', ') || 'Anywhere'} <br />
          <strong>Salary Range:</strong> ${formatCurrency(filters.salary_min)} — ${formatCurrency(filters.salary_max)}
        </Alert>
      ) : null}

      <div className="job-list">
        {results.map((job) => (
          <JobCard key={job.external_id} job={job} />
        ))}
      </div>

    </Container>
  );
};

export default Results;
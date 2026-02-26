import { useState } from 'react';
import api from '../services/api';
import { Container, Row, Col, Spinner, Stack } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import PreferencesSummary from '../components/PreferencesSummary';
import DashboardCard from '../components/DashboardCard';
import DataPullControl from '../components/DataPullControl';
import PreferencesForm from '../components/PreferencesForm';
import SavedJobs from '../components/SavedJobs';

const Dashboard = () => {
  const { user, login, loading: authLoading, notify } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [updating, setUpdating] = useState(false);

  const handleUpdate = async (formData) => {
    setUpdating(true);
    try {
      const response = await api.put('/auth/preferences', formData);
      const token = localStorage.getItem('token');
      login(token, response.data);
      notify("Preferences saved successfully!")
      setIsEditing(false);
    } catch (error) {
      notify("Failed to save preferences.", "danger");
    } finally {
      setUpdating(false);
    }
  };

  if (authLoading) {
    return (
      <Container className="d-flex justify-content-center align-items-center vh-100">
        <Spinner animation="border" variant="primary" />
      </Container>
    );
  }

  if (!user) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="grow" size="sm" variant="secondary" />
        <p className="text-muted">Loading preferences...</p>
      </Container>
    );
  }

  return (
    <Container className="my-4 animate-fade-in">
      <h2 className="mb-4 fw-bold">Welcome, {user?.name?.split(' ')[0] || 'User'}</h2>
      <Row className="g-4">
        <Col lg={8}>
          <Stack gap={4}>
            {isEditing ? (
              <PreferencesForm
                initialData={user?.preferences || {
                  target_roles: [],
                  skills: [],
                  desired_locations: [],
                  salary_min: 0,
                  salary_max: 150000
                }}
                onSearch={handleUpdate}
                onCancel={() => setIsEditing(false)}
                isSubmitting={updating}
              />
            ) : (
              <PreferencesSummary
                preferences={user?.preferences}
                onEdit={() => setIsEditing(true)}
              />
            )}

            <DashboardCard
              title="Saved for Later"
              icon={<i className="bi bi-bookmark-heart"></i>}
            >
              <SavedJobs />
            </DashboardCard>
          </Stack>
        </Col>

        <Col lg={4}>
          <Stack gap={4}>
            <DashboardCard
              title="Search Insight"
              icon={<i className="bi bi-cpu"></i>}
            >
              <p className="small text-muted mb-0">
                The AI agent is optimizing for <strong>{user?.preferences?.skills?.length || 0}</strong> listed skills.
              </p>
            </DashboardCard>
            <DataPullControl />
          </Stack>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
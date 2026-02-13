import React, { useState } from 'react';
import api from '../services/api';
import PreferencesSummary from '../components/PreferencesSummary';
import DashboardCard from '../components/DashboardCard';
import { Container, Row, Col, Spinner } from 'react-bootstrap';
import SearchForm from '../components/SearchForm';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, login, loading: authLoading } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [updating, setUpdating] = useState(false);

  const handleUpdate = async (formData) => {
    setUpdating(true);
    try {
      const response = await api.put('/auth/preferences', formData);
      const token = localStorage.getItem('token');
      login(token, response.data);
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update preferences on dashboard:", error);
      alert("Could not save changes. Please try again.");
    } finally {
      setUpdating(false);
    }
  };

if (authLoading || !user) {
    return (
      <Container className="d-flex flex-column justify-content-center align-items-center vh-100">
        <Spinner animation="border" variant="primary" size="lg" />
        <p className="mt-3 text-muted fw-medium">Syncing your profile...</p>
      </Container>
    );
  }

  return (
    <Container className="my-4 animate-fade-in">
      <h2 className="mb-4 fw-bold">Welcome, {user?.full_name || 'User'}</h2>
      <Row className="g-4">
        <Col lg={8}>
          {isEditing ? (
            <SearchForm
              initialData={user?.preferences}
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
        </Col>

        <Col lg={4}>
          <DashboardCard
            title="Search Insight"
            icon={<i className="bi bi-cpu"></i>}
          >
            <p className="small text-muted mb-0">
              The AI agent is optimizing for <strong>{user?.preferences?.skills?.length || 0}</strong> listed skills.
            </p>
          </DashboardCard>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
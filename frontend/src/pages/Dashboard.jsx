import React, { useEffect, useState } from 'react';
import api from '../services/api';
import PreferencesSummary from '../components/PreferencesSummary';
import DashboardCard from '../components/DashboardCard';
import { Container, Row, Col, Spinner } from 'react-bootstrap';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get('/auth/me');
        setUser(res.data);
      } catch (err) {
        console.error("Dashboard load error", err);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (loading) return <Container className="mt-5 text-center"><Spinner animation="border" /></Container>;

  return (
    <Container className="my-4">
      <h2 className="mb-4">Welcome, {user?.name}</h2>
      <Row className="g-4">

        <Col lg={8}>
          <PreferencesSummary preferences={user?.preferences} />
        </Col>

        <Col lg={4}>
          <DashboardCard
            title="Quick Tip"
            icon={<i className="bi bi-lightbulb"></i>}
          >
            <p className="small text-muted mb-0">
              Your AI is currently analyzing <strong>{user?.preferences?.skills?.length || 0}</strong> {user?.preferences?.skills?.length === 1 ? " skill" : " skills"}.
              Keep them updated for better matches!
            </p>
            
          </DashboardCard>
        </Col>

      </Row>
    </Container>
  );
};

export default Dashboard;
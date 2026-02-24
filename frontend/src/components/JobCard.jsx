import { Card, Badge, Button, Stack, Row, Col, Spinner } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const JobCard = ({ job, initialSaved, onUnsave }) => {
  const {
    title,
    company,
    location,
    salary_range,
    skills_matched = ["Skill 1", "Skill 2", "Skill 3"],
    description,
    match_score,
    url
  } = job;

  const { user } = useAuth();
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsSaved(initialSaved);
  }, [initialSaved]);

  const handleSaveJob = async () => {
    if (!user?.id || isSaved || isLoading) return;
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/interactions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.id,
          job_id: job.id || job._id,
          interaction_type: 'saved'
        }),
      });
      if (response.ok) {
        setIsSaved(true);
      }
    } catch (error) {
      console.error("Save failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUnsaveJob = async () => {
    if (!user?.id || isLoading) return;
    setIsLoading(true);

    try {
      const getRes = await fetch(`http://localhost:8000/interactions/user/${user.id}`);
      const interactions = await getRes.json();
      const target = interactions.find(i => i.job_id === (job.id || job._id));

      if (target) {
        const delRes = await fetch(`http://localhost:8000/interactions/${target.id}`, {
          method: 'DELETE',
        });

        if (delRes.ok) {
          setIsSaved(false);
          if (onUnsave) onUnsave();
        }
      }
    } catch (error) {
      console.error("Unsave failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatSalary = (number) => {
    return new Intl.NumberFormat('en-US').format(number);
  };

  return (
    <Card className="mb-3 border-0 shadow-sm hover-shadow transition-all w-100 text-start">
      <Card.Body className="p-4">
        <Row className="align-items-start">
          <Col>
            <div className="d-flex align-items-center mb-1">
              <Card.Title className="mb-2 fw-bold text-primary fs-5">
                {title}
              </Card.Title>
              {match_score && (
                <Badge bg="info" className="ms-2 px-2 py-1">
                  {match_score}% Match
                </Badge>
              )}
            </div>
            <Card.Subtitle className="mt-1 mb-3 text-muted fw-medium">
              <i className="bi bi-building me-1"></i> {company}
              <span className="mx-2 text-silver">|</span>
              <i className="bi bi-geo-alt me-1"></i> {location}
            </Card.Subtitle>
          </Col>
          <Col xs="auto" className="text-end">
            <div className="fw-bold text-success">
              ${formatSalary(salary_range.min)} - {formatSalary(salary_range.max)}
            </div>
          </Col>
        </Row>

        <Card.Text className="text-secondary small mb-3 line-clamp-2">
          {description}
        </Card.Text>

        <div className="d-flex mb-3">
          <i className='bi bi-lightning-fill text-warning'></i>
          <div className="small fw-bold text-muted mb-2 uppercase tracking-wider" style={{ fontSize: '0.8rem' }}>
            TOP MATCHING SKILLS:
          </div>
          <div>
            <Stack direction="horizontal" gap={2} className="flex-wrap mx-2">
              {skills_matched.map((skill, index) => (
                <Badge key={index} pill bg="light" text="dark" className="border">
                  {skill}
                </Badge>
              ))}
            </Stack>
          </div>
        </div>

        <div className="d-flex justify-content-between align-items-center mt-auto pt-3 border-top">
          <Button
            variant="outline-primary"
            size="sm"
            className="fw-bold px-3"
            onClick={() => window.open(url, '_blank')}
          >
            View Posting <i className="bi bi-box-arrow-up-right ms-1"></i>
          </Button>

          <div className="d-flex align-items-center">
            {isSaved ? (
              <Stack direction="horizontal" gap={3}>
                <span className="text-success small fw-medium">
                  <i className="bi bi-bookmark-check-fill me-1"></i> Saved
                </span>
                <Button
                  variant="outline-danger"
                  size="sm"
                  className="py-1 px-2"
                  style={{ fontSize: '0.7rem', lineHeight: '1' }}
                  onClick={handleUnsaveJob}
                  disabled={isLoading}
                >
                  {isLoading ? <Spinner animation="border" size="sm" /> : "Unsave"}
                </Button>
              </Stack>
            ) : (
              <Button
                variant="link"
                className="text-decoration-none p-0 small text-muted"
                onClick={handleSaveJob}
                disabled={isLoading}
              >
                {isLoading ? <Spinner animation="border" size="sm" /> : (
                  <><i className="bi bi-bookmark me-1"></i> Save for later</>
                )}
              </Button>
            )}
          </div>
        </div>
      </Card.Body>
    </Card>
  );
};

export default JobCard;
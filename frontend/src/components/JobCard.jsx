import { Card, Badge, Button, Stack, Row, Col, Spinner } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const JobCard = ({ job, initialSaved, onUnsave }) => {
  const { title, company, location, salary_range, url } = job;
  const { user } = useAuth();
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [matchData, setMatchData] = useState(null);
  const fetch_url = import.meta.env.VITE_API_URL;

  useEffect(() => {
    setIsSaved(initialSaved);
    const fetchMatchScore = async () => {
      if (!user?.id) return;
      try {
        const res = await fetch(`${fetch_url}/matches/user/${user.id}/job/${job.id || job._id}`);
        if (res.ok) {
          const data = await res.json();
          setMatchData(data);
        }
      } catch (err) {
        console.error("Error fetching match score:", err);
      }
    };

    fetchMatchScore();
  }, [initialSaved, user?.id, job.id, job._id, fetch_url]);

  const handleSaveJob = async () => {
    if (!user?.id || isSaved || isLoading) return;
    setIsLoading(true);
    try {
      const response = await fetch(`${fetch_url}/interactions/`, {
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
      const getRes = await fetch(`${fetch_url}/interactions/user/${user.id}`);
      const interactions = await getRes.json();
      const target = interactions.find(i => i.job_id === (job.id || job._id));

      if (target) {
        const delRes = await fetch(`${fetch_url}/interactions/${target.id}`, {
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

  const missingSkills = matchData?.missing_skills || job.skills_required?.filter(
    (skill) => !user?.preferences?.skills?.some(
      (userSkill) => userSkill.toLowerCase() === skill.toLowerCase()
    )
  ) || [];

  const getScoreColor = (score) => {
    const s = score * 100;
    if (s >= 80) return 'success';
    if (s >= 50) return 'warning';
    return 'danger';
  };

  const formatSalary = (num) => new Intl.NumberFormat('en-US').format(num);

  return (
    <Card className="mb-3 border-0 shadow-sm hover-shadow transition-all w-100 text-start">
      <Card.Body className="p-4">
        <Row className="align-items-center">
          <Col xs="auto" className="pe-4 border-end">
            {matchData ? (
              <div className="text-center">
                <div
                  className={`d-flex align-items-center justify-content-center border border-2 border-${getScoreColor(matchData.score)} rounded-circle shadow-sm`}
                  style={{ width: '55px', height: '55px', backgroundColor: '#fff' }}
                >
                  <span className={`fw-bold text-${getScoreColor(matchData.score)}`} style={{ fontSize: '0.9rem' }}>
                    {Math.round(matchData.score * 100)}%
                  </span>
                </div>
                <div className="text-muted fw-bold mt-1" style={{ fontSize: '0.6rem', letterSpacing: '0.5px' }}>
                  AI MATCH
                </div>
              </div>
            ) : (
              <div className="text-center" style={{ width: '55px' }}>
                <Spinner animation="border" size="md" variant="secondary" />
              </div>
            )}
          </Col>

          <Col className="ps-4">
            <Card.Title className="mb-1 fw-bold text-primary fs-5">
              {title}
            </Card.Title>
            <Card.Subtitle className="mb-3 text-muted fw-medium">
              <i className="bi bi-building me-1"></i> {company}
              <span className="mx-2 text-silver">|</span>
              <i className="bi bi-geo-alt me-1"></i> {location}
            </Card.Subtitle>
          </Col>

          <Col xs="auto" className="text-end">
            <div className="fw-bold text-success fs-5">
              ${formatSalary(salary_range.min)} - {formatSalary(salary_range.max)}
            </div>
          </Col>
        </Row>

        <hr className="my-3 opacity-10" />

        <div className="d-flex align-items-start mb-3">
          <i className='bi bi-lightning-fill text-warning me-2 mt-1'></i>
          <div>
            <div className="small fw-bold text-muted mb-2 uppercase tracking-wider" style={{ fontSize: '0.75rem' }}>
              MISSING SKILLS:
            </div>
            <Stack direction="horizontal" gap={2} className="flex-wrap">
              {missingSkills.length > 0 ? (
                missingSkills.map((skill, index) => (
                  <Badge key={index} pill bg="light" text="dark" className="border fw-normal text-secondary" style={{ fontSize: '0.7rem' }}>
                    {skill}
                  </Badge>
                ))
              ) : (
                <span className="text-success small" style={{ fontSize: '0.75rem' }}>
                  <i className="bi bi-check-circle-fill me-1"></i> You have all required skills!
                </span>
              )}
            </Stack>
          </div>
        </div>

        <div className="d-flex justify-content-between align-items-center mt-auto pt-2">
          <Button variant="outline-primary" size="sm" className="fw-bold px-3" onClick={() => window.open(url, '_blank')}>
            View Posting <i className="bi bi-box-arrow-up-right ms-1"></i>
          </Button>

          <div className="d-flex align-items-center">
            {isSaved ? (
              <Stack direction="horizontal" gap={3}>
                <span className="text-success small fw-medium">
                  <i className="bi bi-bookmark-check-fill me-1"></i> Saved
                </span>
                <Button variant="outline-danger" size="sm" className="py-1 px-2" style={{ fontSize: '0.7rem' }} onClick={handleUnsaveJob} disabled={isLoading}>
                  {isLoading ? <Spinner animation="border" size="sm" /> : "Unsave"}
                </Button>
              </Stack>
            ) : (
              <Button variant="link" className="text-decoration-none p-0 small text-muted" onClick={handleSaveJob} disabled={isLoading}>
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
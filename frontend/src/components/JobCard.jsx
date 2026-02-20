import { Card, Badge, Button, Stack, Row, Col } from 'react-bootstrap';

const JobCard = ({ job }) => {
  const {
    title,
    company,
    location,
    salary_range,
    skills_matched = [],
    description,
    match_score,
    url
  } = job;

  const formatSalary = (number, locale = 'en-US') => {
    return new Intl.NumberFormat(locale).format(number);
  };

  return (
    <Card className="mb-3 border-0 shadow-sm hover-shadow transition-all">
      <Card.Body className="p-4">
        <Row className="align-items-start">
          <Col>
            <div className="d-flex align-items-center mb-1">
              <Card.Title className="mb-0 fw-bold text-primary fs-5">
                {title}
              </Card.Title>
              {match_score && (
                <Badge bg="info" className="ms-2 px-2 py-1">
                  {match_score}% Match
                </Badge>
              )}
            </div>
            <Card.Subtitle className="mb-3 text-muted fw-medium">
              <i className="bi bi-building me-1"></i> {company}
              <span className="mx-2 text-silver">|</span>
              <i className="bi bi-geo-alt me-1"></i> {location}
            </Card.Subtitle>
          </Col>
          <Col xs="auto" className="text-end">
            <div className="fw-bold text-success">${formatSalary(salary_range.min)} - {formatSalary(salary_range.max)}</div>
          </Col>
        </Row>

        <Card.Text className="text-secondary small mb-3 line-clamp-2">
          {description}
        </Card.Text>

        <div className="mb-3">
          <div className="small fw-bold text-muted mb-2 uppercase tracking-wider" style={{ fontSize: '0.7rem' }}>
            TOP MATCHING SKILLS
          </div>
          <Stack direction="horizontal" gap={1} className="flex-wrap">
            {skills_matched.map((skill, index) => (
              <Badge key={index} pill bg="light" text="dark" className="border">
                {skill}
              </Badge>
            ))}
          </Stack>
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
          <Button variant="link" className="text-decoration-none text-muted p-0 small">
            Save for later
          </Button>
        </div>
      </Card.Body>
    </Card>
  );
};

export default JobCard;
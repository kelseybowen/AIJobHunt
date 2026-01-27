import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const PageHeader = ({ title, subtitle }) => {
  return (
    <div className="bg-light py-5 mb-4 border-bottom">
      <Container>
        <Row className="justify-content-center text-center">
          <Col md={8} lg={6}>
            <h1 className="fw-bold display-5 mb-2">{title}</h1>
            {subtitle ? (
              <p className="lead text-muted mb-0">{subtitle}</p>
            ) : null}
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default PageHeader;
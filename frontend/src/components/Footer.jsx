import React from 'react';
import { Container, Row, Col, Nav } from 'react-bootstrap';
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="bg-light border-top py-4 mt-auto">
      <Container>
        <Row className="align-items-center">
          <Col md={6} className="text-center text-md-start">
            <span className="text-muted small">
              © 2026 AI Job Search Capstone. Developed for educational purposes.
            </span>
          </Col>
          <Col md={6}>
            <Nav className="justify-content-center justify-content-md-end">
              <Nav.Link as={Link} to="/privacy" className="text-muted small">
                Privacy Policy
              </Nav.Link>
              <Nav.Link as={Link} to="/terms" className="text-muted small">
                Terms of Use
              </Nav.Link>
            </Nav>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
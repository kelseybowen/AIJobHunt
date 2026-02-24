import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';

const FeatureGrid = ({ items, columns = 4 }) => {
  return (
    <Row className="g-4 mb-5 justify-content-center">
      {items.map((item, idx) => (
        <Col md={columns} key={idx}>
          <Card className="h-100 border-0 shadow text-center p-3 hover-shadow transition-all">
            <Card.Body>
              {item.icon && (
                <div className="mb-3 text-primary fs-2">
                  <i className={`bi ${item.icon}`}></i>
                </div>
              )}
              <Card.Title className="fw-bold">{item.title}</Card.Title>
              <Card.Text className="text-secondary small">
                {item.text}
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  );
};

export default FeatureGrid;
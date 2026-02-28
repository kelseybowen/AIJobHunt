import { Container, Row, Col, Card, Badge } from 'react-bootstrap';
import FeatureGrid from '../components/FeatureGrid';

const About = () => {
  const aboutFeatures = [
    {
      title: "Holistic Skill Mapping",
      text: "We move beyond keyword matching. Our engine analyzes core competencies to identify matches based on your actual capabilities.",
      icon: "bi-cpu"
    },
    {
      title: "Dynamic Optimization",
      text: "As your experience grows, so does your search. The AI agent adapts to your evolving preferences in real-time.",
      icon: "bi-lightning-charge"
    },
    {
      title: "Precision Filtering",
      text: "Cut through the clutter with opportunities that respect your salary, location, and professional goals.",
      icon: "bi-filter-circle"
    }
  ];
  return (
    <div>
      <Container className="py-5 animate-fade-in">
        <div className="text-center mb-5">
          <h1 className="display-4 fw-bold text-primary mb-3">About AI Job Hunt</h1>
          <p className="lead text-secondary mx-auto" style={{ maxWidth: '700px' }}>
            Bridging the gap between the skills you have and the roles you want.
          </p>
        </div>

        <Row className="mb-5 mx-auto align-items-center">
          <Col lg={8} className='mx-auto'>
            <p className="text-secondary text-center fs-5">
              Finding your next opportunity shouldn't be a full-time job.
              In a world where job boards are overflowing with noise, we believe the
              search for meaningful work should be high-signal and low-friction. 
              Our mission is to transform the job hunt from a daunting administrative
              burden into a streamlined experience. By letting technology handle the
              heavy lifting of discovery, you can focus on what actually lands the job: 
              preparation and growth.
            </p>
          </Col>
        </Row>

        <h3 className="text-center fw-bold mb-0 text-uppercase fs-5 text-primary tracking-wider">How it works</h3>
        <Row>
          <FeatureGrid items={aboutFeatures} columns={4} />
        </Row>

        <Card className="border-0 p-4 shadow text-center">
          <Row className="align-items-center">
            <Col >
              <h4 className="fw-bold">Powered by Modern Architecture</h4>
              <p className="mb-0 text-silver medium">
                Built using <strong>FastAPI</strong> for high-performance logic,
                <strong> MongoDB</strong> for flexible data storage, and
                <strong> React</strong> for a responsive user experience.
              </p>
            </Col>
          </Row>
        </Card>
      </Container>
    </div>
  )
}
export default About
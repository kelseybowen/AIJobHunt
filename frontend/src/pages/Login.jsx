import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Alert, Container, Row, Col, Card, Form, Button, InputGroup, Spinner } from 'react-bootstrap';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [authError, setAuthError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting } 
  } = useForm();

  const onSubmit = async (data) => {
    setAuthError(null);
    try {
      const response = await api.post('/auth/login', data);
      if (response.data.user) {
        login(response.data.access_token, response.data.user);
        navigate('/dashboard');
      } else {
        console.error("User data missing from server response");
        setAuthError("Server error: Missing user profile data.");
      }
    } catch (error) {
      const message = error.response?.data?.detail || 'An unexpected error occurred. Please try again.';
      setAuthError(message);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={6} lg={4}>
          <Card className="shadow-sm border-0">
            <Card.Body className="p-4">
              <h2 className="text-center mb-4 fw-bold">Login</h2>

              {authError && (
                <Alert variant="danger" className="py-2 small text-center">
                  {authError}
                </Alert>
              )}

              <Form onSubmit={handleSubmit(onSubmit)}>

                {/* Email Field */}
                <Form.Group className="mb-3">
                  <Form.Label className="small fw-bold text-muted">Email Address</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="email@example.com"
                    {...register('email', {
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                      }
                    })}
                    isInvalid={!!errors.email}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.email?.message}
                  </Form.Control.Feedback>
                </Form.Group>

                {/* Password Field */}
                <Form.Group className="mb-4">
                  <Form.Label className="small fw-bold text-muted">Password</Form.Label>
                  <InputGroup hasValidation>
                    <Form.Control
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      {...register('password', {
                        required: 'Password is required',
                        minLength: { value: 8, message: 'Password must be at least 8 characters' }
                      })}
                      isInvalid={!!errors.password}
                    />
                    <Button 
                      variant="outline-secondary" 
                      onClick={() => setShowPassword(!showPassword)}
                      style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                    >
                      <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                    </Button>
                    <Form.Control.Feedback type="invalid">
                      {errors.password?.message}
                    </Form.Control.Feedback>
                  </InputGroup>
                </Form.Group>

                <div className="text-center">
                  <Button 
                    type="submit" 
                    disabled={isSubmitting} 
                    variant="primary" 
                    className="w-100 py-2 fw-semibold mb-3"
                  >
                    {isSubmitting ? (
                      <>
                        <Spinner animation="border" size="sm" className="me-2" />
                        Signing in...
                      </>
                    ) : (
                      'Sign In'
                    )}
                  </Button>

                  <p className="small text-muted mt-2">
                    Need an account? <Link to="/register" className="text-decoration-none">Create Account</Link>
                  </p>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Login;
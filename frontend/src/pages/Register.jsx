import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Alert, Container, Row, Col, Card, Form, Button, InputGroup } from 'react-bootstrap';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const [regError, setRegError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const { register, handleSubmit, watch, formState: { errors, isSubmitting } } = useForm();
  const password = watch("password", "");

  const onSubmit = async (data) => {
    setRegError(null);
    try {
      const { confirmPassword, ...registerData } = data;
      const response = await api.post('/auth/register', registerData);
      if (response.data && response.data.user && response.data.access_token) {
        login(response.data.access_token, response.data.user);
        navigate('/dashboard');
      } else {
        console.error("Malformed response from server:", response.data);
        setRegError("Account created, but we couldn't load your profile. Please try logging in.");
      }
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed. Please try again.';
      setRegError(message);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={6} lg={5}>
          <Card className="shadow-sm border-0">
            <Card.Body className="p-4">
              <h2 className="text-center mb-4">Create Account</h2>

              {regError && (
                <Alert variant="danger" className="py-2 small text-center">
                  {regError}
                </Alert>
              )}

              <Form onSubmit={handleSubmit(onSubmit)}>
                {/* Full Name Field */}
                <Form.Group className="mb-3">
                  <Form.Label>Full Name</Form.Label>
                  <Form.Control
                    {...register("name", { required: "Name is required" })}
                    isInvalid={!!errors.name}
                  />
                  <Form.Control.Feedback type="invalid">{errors.name?.message}</Form.Control.Feedback>
                </Form.Group>

                {/* Email Field */}
                <Form.Group className="mb-3">
                  <Form.Label>Email Address</Form.Label>
                  <Form.Control
                    type="email"
                    {...register("email", { required: "Email is required" })}
                    isInvalid={!!errors.email}
                  />
                  <Form.Control.Feedback type="invalid">{errors.email?.message}</Form.Control.Feedback>
                </Form.Group>

                {/* Password Field */}
                <Form.Group className="mb-4">
                  <Form.Label>Password</Form.Label>
                  <InputGroup hasValidation>
                    <Form.Control
                      type={showPassword ? "text" : "password"}
                      {...register("password", {
                        required: "Password is required",
                        minLength: { value: 8, message: "At least 8 characters" }
                      })}
                      isInvalid={!!errors.password}
                    />
                    {/* Password visibility toggle */}
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

                {/* Confirm Password Field*/}
                <Form.Group className="mb-4">
                  <Form.Label>Confirm Password</Form.Label>
                  <InputGroup hasValidation>
                    <Form.Control
                      type={showPassword ? "text" : "password"}
                      {...register("confirmPassword", {
                        required: "Please confirm your password",
                        validate: (value) => value === password || "Passwords do not match"
                      })}
                      isInvalid={!!errors.confirmPassword}
                    />
                    <Form.Control.Feedback type="invalid">{errors.confirmPassword?.message}</Form.Control.Feedback>
                  </InputGroup>
                </Form.Group>

                <Button type="submit" variant="primary" className="w-100" disabled={isSubmitting}>
                  {isSubmitting ? 'Creating Account...' : 'Register'}
                </Button>
              </Form>

              <div className="text-center mt-3">
                <p className="small text-muted mb-0">
                  Already have an account?{' '}
                  <Link to="/login" className="text-decoration-none">
                    Log In
                  </Link>
                </p>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Register;
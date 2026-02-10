import { useForm } from 'react-hook-form';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';
import { Alert } from 'react-bootstrap';

const Login = () => {
  const [authError, setAuthError] = useState(null);
  const navigate = useNavigate();
  const { login } = useAuth();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();

  const onSubmit = async (data) => {
    setAuthError(null);
    try {
      const response = await api.post('/auth/login', data);
      login(response.data.access_token);
      navigate('/dashboard');
    } catch (error) {
      const message = error.response?.data?.detail || 'An unexpected error occurred. Please try again.';
      setAuthError(message);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-12 col-md-6 col-lg-4">
          <div className="card shadow-sm border-0">
            <div className="card-body p-4">
              <h2 className="text-center mb-4 fw-bold">Login</h2>

              {authError && (
                <Alert variant="danger" className="py-2 small text-center">
                  {authError}
                </Alert>
              )}

              <form onSubmit={handleSubmit(onSubmit)}>
                {/* Email Field */}
                <div className="mb-3">
                  <label className="form-label small fw-bold text-muted">Email Address</label>
                  <input
                    type="email"
                    {...register('email', {
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                      }
                    })}
                    className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                    placeholder="email@example.com"
                  />
                  {errors.email && (
                    <div className="invalid-feedback">{errors.email.message}</div>
                  )}
                </div>

                {/* Password Field */}
                <div className="mb-4">
                  <label className="form-label small fw-bold text-muted">Password</label>
                  <input
                    type="password"
                    {...register('password', {
                      required: 'Password is required',
                      minLength: { value: 8, message: 'Password must be at least 8 characters' }
                    })}
                    className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                    placeholder="••••••••"
                  />
                  {errors.password && (
                    <div className="invalid-feedback">{errors.password.message}</div>
                  )}
                </div>

                <div className="text-center mt-3">
                  {/* Submit Button */}
                  <button type="submit" disabled={isSubmitting} className="btn btn-primary w-full py-2 fw-semibold mx-2">
                    {isSubmitting ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Signing in...
                      </>
                    ) : (
                      'Sign In'
                    )}
                  </button>
                  <div className="text-center mt-3">
                    <p className="small text-muted">
                      Need an account? <a href="/register" className="text-decoration-none">Create Account</a>
                    </p>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
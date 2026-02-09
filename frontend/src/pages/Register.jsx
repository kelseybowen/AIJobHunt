import { useForm } from 'react-hook-form';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm();

  // Watch the password field to compare to confirmPassword
  const password = watch("password", "");

  const onSubmit = async (data) => {
    try {
      // Send data to Python backend
      const response = await api.post('/auth/register', {
        name: data.name,
        email: data.email,
        password: data.password
      });
      
      // Auto-login after successful registration
      login(response.data.access_token);
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration Failed:', error.response?.data?.message || 'Server error');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-12 col-md-8 col-lg-5">
          <div className="card shadow-sm border-0">
            <div className="card-body p-4">
              <h2 className="text-center mb-4 fw-bold">Create Account</h2>
              
              <form onSubmit={handleSubmit(onSubmit)}>
                {/* Full Name */}
                <div className="mb-3">
                  <label className="form-label small fw-bold text-muted">Full Name</label>
                  <input
                    type="text"
                    {...register('name', { required: 'Name is required' })}
                    className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                    placeholder="Kelsey Bowen"
                  />
                  {errors.name && <div className="invalid-feedback">{errors.name.message}</div>}
                </div>

                {/* Email Address */}
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
                  {errors.email && <div className="invalid-feedback">{errors.email.message}</div>}
                </div>

                {/* Password */}
                <div className="mb-3">
                  <label className="form-label small fw-bold text-muted">Password</label>
                  <input
                    type="password"
                    {...register('password', { 
                      required: 'Password is required',
                      minLength: { value: 8, message: 'Must be at least 8 characters' }
                    })}
                    className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                    placeholder="••••••••"
                  />
                  {errors.password && <div className="invalid-feedback">{errors.password.message}</div>}
                </div>

                {/* Confirm Password */}
                <div className="mb-4">
                  <label className="form-label small fw-bold text-muted">Confirm Password</label>
                  <input
                    type="password"
                    {...register('confirmPassword', { 
                      required: 'Please confirm your password',
                      validate: (value) => value === password || "Passwords do not match"
                    })}
                    className={`form-control ${errors.confirmPassword ? 'is-invalid' : ''}`}
                    placeholder="••••••••"
                  />
                  {errors.confirmPassword && (
                    <div className="invalid-feedback">{errors.confirmPassword.message}</div>
                  )}
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn btn-primary w-100 py-2 fw-semibold"
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Creating Account...
                    </>
                  ) : (
                    'Register'
                  )}
                </button>
              </form>
              
              <div className="text-center mt-3">
                <p className="small text-muted">
                  Already have an account? <a href="/login" className="text-decoration-none">Login</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
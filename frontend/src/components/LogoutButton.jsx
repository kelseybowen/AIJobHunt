import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LogoutButton = ({ variant = "outline-danger", size = "sm", className = "" }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <button 
      onClick={handleLogout} 
      className={`btn btn-${variant} btn-${size} ${className} d-flex align-items-center gap-2`}
      title="Sign Out"
    >
      Logout
    </button>
  );
};

export default LogoutButton;
import PageHeader from "../components/PageHeader"

const Login = () => {

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const onSubmit = async (data) => {
    try {
      // Send data to Python backend
      const response = await api.post('/auth/login', data);
      console.log('Login Success:', response.data);
      // TODO: Save the token and redirect to Dashboard
    } catch (error) {
      console.error('Login Failed:', error.response?.data?.message || 'Server error');
    }
  };

  return (
    <PageHeader title="Login" />

  )
}

export default Login;
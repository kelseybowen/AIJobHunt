import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import Search from './pages/Search';
import Results from './pages/Results';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  const [msg, setMsg] = useState('Loading...')

  useEffect(() => {
    fetch('/api')
      .then(res => res.json())
      .then(data => setMsg(data.message))
      .catch(err => setMsg("API not connected"))
  }, [])

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/search" element={<Search />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </div>
  )
}

export default App

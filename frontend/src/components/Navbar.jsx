import { Link } from "react-router-dom"

const Navbar = () => {
  return (
    <header className="w-full bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto w-full flex justify-between items-center px-6">
        <h1 className="text-xl font-bold py-4">AI Job Hunt</h1>
        <nav className="flex items-center gap-x-6">
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/about">About</Link>
          <Link to="/search">Search</Link>
          <Link to="/results">Results</Link>
        </nav>
      </div>
    </header>
  )
}
export default Navbar
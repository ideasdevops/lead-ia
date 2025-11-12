import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import PrivateRoute from './components/PrivateRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Search from './pages/Search'
import Results from './pages/Results'
import Users from './pages/Users'
import Roles from './pages/Roles'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout />
              </PrivateRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="search" element={<Search />} />
            <Route path="results" element={<Results />} />
            <Route path="users" element={<Users />} />
            <Route path="roles" element={<Roles />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App


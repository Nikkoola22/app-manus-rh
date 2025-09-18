import { useState } from 'react'
import SimpleLogin from './components/SimpleLogin'
import Dashboard from './components/Dashboard'
import './index.css'
import './styles/dialog-fixes.css'

function App() {
  const [user, setUser] = useState(null)

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    setUser(null)
  }

  return (
    <div className="App">
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <SimpleLogin onLogin={handleLogin} />
      )}
    </div>
  )
}

export default App

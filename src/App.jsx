import { useState, useEffect } from 'react'
import TestLogin from './TestLogin'
import TestDialog from './TestDialog'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import api from './services/api'
import './index.css'
import './styles/dialog-fixes.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [useTestMode, setUseTestMode] = useState(true)

  useEffect(() => {
    checkSession()
  }, [])

  const checkSession = async () => {
    try {
      const response = await api.checkSession()
      const data = await response.json()
      
      if (data.authenticated) {
        setUser(data.user)
      }
    } catch (err) {
      console.error('Erreur lors de la vérification de session:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    setUser(null)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <div className="text-center animate-fade-in">
          <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg mx-auto animate-bounce-in">
            <div className="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
          </div>
          <p className="text-gray-600 font-medium">Chargement de l'application...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="App">
      {useTestMode ? (
        <div className="min-h-screen">
          <div className="p-6 bg-gradient-to-r from-blue-100 to-indigo-100 border-b border-blue-200 shadow-lg">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Mode Test - Diagnostic de connexion</h3>
            <div className="flex gap-4">
              <button 
                onClick={() => setUseTestMode(false)}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5"
              >
                Passer au mode normal
              </button>
              <button 
                onClick={() => setUseTestMode('dialog')}
                className="px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5"
              >
                Tester les dialogs
              </button>
            </div>
          </div>
          <div className="animate-fade-in">
            {useTestMode === 'dialog' ? <TestDialog /> : <TestLogin />}
          </div>
        </div>
      ) : (
        user ? (
          <Dashboard user={user} onLogout={handleLogout} />
        ) : (
          <Login onLogin={handleLogin} />
        )
      )}
    </div>
  )
}

export default App

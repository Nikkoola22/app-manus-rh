import { useState } from 'react'

const TestLogin = () => {
  const [email, setEmail] = useState('admin@exemple.com')
  const [password, setPassword] = useState('admin123')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  const testLogin = async () => {
    setLoading(true)
    setResult('')
    
    try {
      console.log('Tentative de connexion avec:', { email, password })
      
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
      })
      
      console.log('Réponse reçue:', response.status, response.statusText)
      
      const data = await response.json()
      console.log('Données reçues:', data)
      
      if (response.ok) {
        setResult(`✅ Connexion réussie ! Utilisateur: ${data.user.prenom} ${data.user.nom} (${data.user.role})`)
      } else {
        setResult(`❌ Erreur: ${data.error || 'Erreur inconnue'}`)
      }
    } catch (error) {
      console.error('Erreur:', error)
      setResult(`❌ Erreur de connexion: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const testSession = async () => {
    try {
      const response = await fetch('/api/auth/check-session', {
        credentials: 'include',
      })
      
      const data = await response.json()
      console.log('Session check:', data)
      
      if (data.authenticated) {
        setResult(`✅ Session active: ${data.user.prenom} ${data.user.nom}`)
      } else {
        setResult('❌ Aucune session active')
      }
    } catch (error) {
      setResult(`❌ Erreur session: ${error.message}`)
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>Test de connexion</h2>
      
      <div style={{ marginBottom: '10px' }}>
        <label>Email:</label><br/>
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)}
          style={{ padding: '5px', width: '200px' }}
        />
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <label>Mot de passe:</label><br/>
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)}
          style={{ padding: '5px', width: '200px' }}
        />
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <button 
          onClick={testLogin} 
          disabled={loading}
          style={{ padding: '10px', marginRight: '10px' }}
        >
          {loading ? 'Connexion...' : 'Tester connexion'}
        </button>
        
        <button 
          onClick={testSession}
          style={{ padding: '10px' }}
        >
          Vérifier session
        </button>
      </div>
      
      {result && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: result.includes('✅') ? '#d4edda' : '#f8d7da',
          border: '1px solid #c3e6cb',
          borderRadius: '4px',
          marginTop: '10px'
        }}>
          {result}
        </div>
      )}
    </div>
  )
}

export default TestLogin





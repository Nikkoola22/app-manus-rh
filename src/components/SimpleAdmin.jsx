import { useState, useEffect } from 'react'

const SimpleAdmin = ({ user }) => {
  const [status, setStatus] = useState('Chargement...')
  const [agents, setAgents] = useState([])

  useEffect(() => {
    const loadData = async () => {
      try {
        setStatus('Connexion en cours...')
        
        const response = await fetch('/api/agents', { 
          credentials: 'include' 
        })
        
        if (response.ok) {
          const data = await response.json()
          setAgents(data)
          setStatus(`✅ ${data.length} agents chargés`)
        } else {
          setStatus(`❌ Erreur: ${response.status}`)
        }
      } catch (error) {
        setStatus(`💥 Erreur: ${error.message}`)
      }
    }

    loadData()
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#333', marginBottom: '20px' }}>
        🔧 Diagnostic Admin
      </h1>
      
      <div style={{ 
        backgroundColor: '#f0f0f0', 
        padding: '15px', 
        borderRadius: '5px',
        marginBottom: '20px'
      }}>
        <h3>👤 Utilisateur connecté :</h3>
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </div>

      <div style={{ 
        backgroundColor: '#e8f4fd', 
        padding: '15px', 
        borderRadius: '5px',
        marginBottom: '20px'
      }}>
        <h3>📊 Status des données :</h3>
        <p><strong>{status}</strong></p>
        <p>Nombre d'agents : {agents.length}</p>
      </div>

      {agents.length > 0 && (
        <div style={{ 
          backgroundColor: '#f0f8f0', 
          padding: '15px', 
          borderRadius: '5px'
        }}>
          <h3>👥 Agents :</h3>
          <ul>
            {agents.slice(0, 3).map(agent => (
              <li key={agent.id}>
                {agent.prenom} {agent.nom} ({agent.role})
              </li>
            ))}
            {agents.length > 3 && <li>... et {agents.length - 3} autres</li>}
          </ul>
        </div>
      )}

      <div style={{ 
        backgroundColor: '#fff3cd', 
        padding: '15px', 
        borderRadius: '5px',
        marginTop: '20px'
      }}>
        <h3>🔍 Instructions :</h3>
        <ol>
          <li>Vérifiez la console du navigateur (F12)</li>
          <li>Regardez s'il y a des erreurs JavaScript</li>
          <li>Vérifiez l'onglet Network pour les requêtes API</li>
        </ol>
      </div>
    </div>
  )
}

export default SimpleAdmin


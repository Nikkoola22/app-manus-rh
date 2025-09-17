import { useState, useEffect } from 'react'

const AdminTest = ({ user, onViewAgent }) => {
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      console.log('🔍 AdminTest: fetchData démarré')
      try {
        const response = await fetch('/api/agents', { credentials: 'include' })
        console.log('🔍 AdminTest: Response status:', response.status)
        
        if (response.ok) {
          const data = await response.json()
          console.log('🔍 AdminTest: Data reçue:', data)
          setAgents(data)
        } else {
          console.log('🔍 AdminTest: Erreur response:', response.status)
        }
      } catch (error) {
        console.log('🔍 AdminTest: Erreur catch:', error)
      } finally {
        console.log('🔍 AdminTest: setLoading(false)')
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  console.log('🔍 AdminTest: Render - loading:', loading, 'agents:', agents.length)

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Admin Test - Chargement...</h1>
        <div className="bg-blue-100 p-4 rounded">
          <p>Chargement des données...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Admin Test - Données chargées</h1>
      
      <div className="bg-green-100 p-4 rounded mb-4">
        <p><strong>Status:</strong> Données chargées avec succès</p>
        <p><strong>Nombre d'agents:</strong> {agents.length}</p>
        <p><strong>Loading state:</strong> {loading.toString()}</p>
      </div>

      <div className="bg-gray-100 p-4 rounded">
        <h3 className="font-bold mb-2">Agents:</h3>
        <ul>
          {agents.slice(0, 5).map(agent => (
            <li key={agent.id} className="py-1">
              {agent.prenom} {agent.nom} ({agent.role})
            </li>
          ))}
          {agents.length > 5 && <li>... et {agents.length - 5} autres</li>}
        </ul>
      </div>

      <div className="mt-4 bg-yellow-100 p-4 rounded">
        <h3 className="font-bold mb-2">User object:</h3>
        <pre className="text-sm">{JSON.stringify(user, null, 2)}</pre>
      </div>
    </div>
  )
}

export default AdminTest


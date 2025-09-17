import { useState, useEffect } from 'react'

const TestAdmin = ({ user }) => {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('🔍 TestAdmin: Début du chargement des données')
        console.log('👤 User:', user)
        
        const response = await fetch('/api/agents', { 
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        console.log('📡 Response status:', response.status)
        console.log('📡 Response headers:', response.headers)
        
        if (response.ok) {
          const data = await response.json()
          console.log('✅ Données reçues:', data)
          setData(data)
        } else {
          const errorData = await response.json()
          console.log('❌ Erreur API:', errorData)
          setError(errorData)
        }
      } catch (err) {
        console.log('💥 Erreur de connexion:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [user])

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Test Admin - Chargement...</h1>
        <div className="bg-blue-100 p-4 rounded">
          <p>Chargement des données en cours...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Test Admin - Erreur</h1>
        <div className="bg-red-100 p-4 rounded">
          <p className="font-bold">Erreur:</p>
          <pre className="mt-2 text-sm">{JSON.stringify(error, null, 2)}</pre>
        </div>
        <div className="mt-4 bg-yellow-100 p-4 rounded">
          <p className="font-bold">User object:</p>
          <pre className="mt-2 text-sm">{JSON.stringify(user, null, 2)}</pre>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Test Admin - Succès</h1>
      <div className="bg-green-100 p-4 rounded">
        <p className="font-bold">Données chargées avec succès!</p>
        <p>Nombre d'agents: {data ? data.length : 0}</p>
      </div>
      <div className="mt-4 bg-gray-100 p-4 rounded">
        <p className="font-bold">Données complètes:</p>
        <pre className="mt-2 text-sm overflow-auto max-h-96">{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  )
}

export default TestAdmin


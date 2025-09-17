import { useState, useEffect } from 'react'

const ServicesDebug = () => {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await fetch('/api/services', { credentials: 'include' })
        if (response.ok) {
          const data = await response.json()
          console.log('🔍 ServicesDebug - Services:', data)
          setServices(data)
        } else {
          console.error('Erreur lors du chargement des services:', response.status)
        }
      } catch (error) {
        console.error('Erreur lors du chargement des services:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchServices()
  }, [])

  if (loading) {
    return <div>Chargement des services...</div>
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Debug Services</h2>
      <div className="space-y-4">
        {services.map((service, index) => (
          <div key={service.id} className="border p-4 rounded">
            <h3 className="font-bold">Service {index + 1}: {service.nom_service}</h3>
            <div className="ml-4">
              <p><strong>ID:</strong> {service.id}</p>
              <p><strong>Responsable ID:</strong> {service.responsable_id || 'Aucun'}</p>
              <p><strong>Responsable:</strong> {service.responsable ? JSON.stringify(service.responsable) : 'Aucun'}</p>
              <p><strong>Nombre d'agents:</strong> {service.nb_agents || 0}</p>
              <p><strong>Date création:</strong> {service.date_creation || 'N/A'}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ServicesDebug


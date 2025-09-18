import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const ResponsableDashboardTest = ({ user }) => {
  const [activeTab, setActiveTab] = useState('demandes-attente')
  const [demandes, setDemandes] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const response = await fetch('/api/demandes', {
        credentials: 'include',
      })
      if (response.ok) {
        const data = await response.json()
        setDemandes(data)
      }
    } catch (err) {
      console.error('Erreur lors du chargement des demandes:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleTabClick = (tabValue) => {
    console.log('Tab clicked:', tabValue)
    setActiveTab(tabValue)
  }

  const demandesEnAttente = demandes.filter(d => d.statut === 'En attente')
  const demandesTraitees = demandes.filter(d => d.statut === 'Approuvée' || d.statut === 'Refusée')

  const tabs = [
    { id: 'demandes-attente', label: `Demandes en attente (${demandesEnAttente.length})` },
    { id: 'demandes-traitees', label: `Demandes traitées (${demandesTraitees.length})` },
    { id: 'mes-demandes', label: 'Mes Demandes (0)' },
    { id: 'agents', label: 'Agents du service (3)' },
    { id: 'arrets-maladie', label: 'Arrêts maladie (0)' },
    { id: 'calendrier', label: 'Calendrier' },
    { id: 'planning', label: 'Planning' }
  ]

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Test des onglets (Version HTML)</h1>
      
      <div className="debug-info p-4 bg-gray-100 rounded">
        <p><strong>Onglet actif:</strong> {activeTab}</p>
        <p><strong>Demandes en attente:</strong> {demandesEnAttente.length}</p>
        <p><strong>Demandes traitées:</strong> {demandesTraitees.length}</p>
      </div>

      {/* Onglets HTML simples */}
      <div className="flex flex-wrap gap-2 mb-6">
        {tabs.map(tab => (
          <Button
            key={tab.id}
            variant={activeTab === tab.id ? "default" : "outline"}
            onClick={() => handleTabClick(tab.id)}
            className={`px-4 py-2 rounded-lg transition-all ${
              activeTab === tab.id 
                ? 'bg-blue-600 text-white shadow-lg' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {tab.label}
          </Button>
        ))}
      </div>

      {/* Contenu des onglets */}
      <div className="tab-content">
        {activeTab === 'demandes-attente' && (
          <Card>
            <CardHeader>
              <CardTitle>Demandes en attente de validation</CardTitle>
              <CardDescription>
                Demandes de congés et RTT à traiter pour votre service
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-4">Chargement...</div>
              ) : demandesEnAttente.length === 0 ? (
                <div className="text-center py-4 text-muted-foreground">
                  Aucune demande en attente
                </div>
              ) : (
                <div>
                  <p>Nombre de demandes en attente: {demandesEnAttente.length}</p>
                  {demandesEnAttente.map(demande => (
                    <div key={demande.id} className="p-2 border rounded mb-2">
                      <p><strong>Type:</strong> {demande.type_absence}</p>
                      <p><strong>Statut:</strong> {demande.statut}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 'demandes-traitees' && (
          <Card>
            <CardHeader>
              <CardTitle>Demandes traitées</CardTitle>
              <CardDescription>
                Historique des demandes validées ou refusées
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Nombre de demandes traitées: {demandesTraitees.length}</p>
            </CardContent>
          </Card>
        )}

        {activeTab === 'mes-demandes' && (
          <Card>
            <CardHeader>
              <CardTitle>Mes Demandes de Congés</CardTitle>
              <CardDescription>
                Créer et suivre vos demandes de congés
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Mes demandes personnelles</p>
            </CardContent>
          </Card>
        )}

        {activeTab === 'agents' && (
          <Card>
            <CardHeader>
              <CardTitle>Agents du service</CardTitle>
              <CardDescription>
                Vue d'ensemble des soldes de congés de votre équipe
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Liste des agents</p>
            </CardContent>
          </Card>
        )}

        {activeTab === 'arrets-maladie' && (
          <Card>
            <CardHeader>
              <CardTitle>Arrêts maladie</CardTitle>
              <CardDescription>
                Gestion des arrêts maladie de votre équipe
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Arrêts maladie</p>
            </CardContent>
          </Card>
        )}

        {activeTab === 'calendrier' && (
          <Card>
            <CardHeader>
              <CardTitle>Calendrier</CardTitle>
              <CardDescription>
                Vue calendrier des congés
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Calendrier</p>
            </CardContent>
          </Card>
        )}

        {activeTab === 'planning' && (
          <Card>
            <CardHeader>
              <CardTitle>Planning</CardTitle>
              <CardDescription>
                Gestion des plannings des agents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Planning</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default ResponsableDashboardTest


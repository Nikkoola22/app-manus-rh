import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const ResponsableDashboardSimple = ({ user }) => {
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

  const handleTabChange = (value) => {
    console.log('Tab changed to:', value)
    setActiveTab(value)
  }

  const demandesEnAttente = demandes.filter(d => d.statut === 'En attente')
  const demandesTraitees = demandes.filter(d => d.statut === 'Approuvée' || d.statut === 'Refusée')

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Tableau de bord Responsable (Version Simple)</h1>
      
      <div className="debug-info p-4 bg-gray-100 rounded">
        <p><strong>Onglet actif:</strong> {activeTab}</p>
        <p><strong>Demandes en attente:</strong> {demandesEnAttente.length}</p>
        <p><strong>Demandes traitées:</strong> {demandesTraitees.length}</p>
      </div>

      <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
        <TabsList>
          <TabsTrigger value="demandes-attente">
            Demandes en attente ({demandesEnAttente.length})
          </TabsTrigger>
          <TabsTrigger value="demandes-traitees">
            Demandes traitées ({demandesTraitees.length})
          </TabsTrigger>
          <TabsTrigger value="mes-demandes">
            Mes Demandes (0)
          </TabsTrigger>
          <TabsTrigger value="agents">
            Agents du service (3)
          </TabsTrigger>
          <TabsTrigger value="arrets-maladie">
            Arrêts maladie (0)
          </TabsTrigger>
          <TabsTrigger value="calendrier">
            Calendrier
          </TabsTrigger>
          <TabsTrigger value="planning">
            Planning
          </TabsTrigger>
        </TabsList>

        <TabsContent value="demandes-attente">
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
        </TabsContent>

        <TabsContent value="demandes-traitees">
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
        </TabsContent>

        <TabsContent value="mes-demandes">
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
        </TabsContent>

        <TabsContent value="agents">
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
        </TabsContent>

        <TabsContent value="arrets-maladie">
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
        </TabsContent>

        <TabsContent value="calendrier">
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
        </TabsContent>

        <TabsContent value="planning">
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
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ResponsableDashboardSimple



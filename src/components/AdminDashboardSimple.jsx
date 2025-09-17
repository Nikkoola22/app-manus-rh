import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Users, Building, Clock, Plus } from 'lucide-react'

const AdminDashboardSimple = ({ user, onViewAgent }) => {
  const [agents, setAgents] = useState([])
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      console.log('🔍 AdminDashboardSimple: fetchData démarré')
      try {
        const [agentsResponse, servicesResponse] = await Promise.all([
          fetch('/api/agents', { credentials: 'include' }),
          fetch('/api/services', { credentials: 'include' })
        ])

        if (agentsResponse.ok) {
          const agentsData = await agentsResponse.json()
          setAgents(agentsData)
          console.log('🔍 AdminDashboardSimple: Agents chargés:', agentsData.length)
        }

        if (servicesResponse.ok) {
          const servicesData = await servicesResponse.json()
          setServices(servicesData)
          console.log('🔍 AdminDashboardSimple: Services chargés:', servicesData.length)
        }
      } catch (err) {
        console.error('Erreur lors du chargement des données:', err)
      } finally {
        console.log('🔍 AdminDashboardSimple: setLoading(false)')
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  console.log('🔍 AdminDashboardSimple: Render - loading:', loading, 'agents:', agents.length, 'services:', services.length)

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Admin Dashboard - Chargement...</h1>
        <div className="bg-blue-100 p-4 rounded">
          <p>Chargement des données en cours...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tableau de Bord Admin</h1>
        <div className="text-sm text-gray-600">
          Connecté en tant que {user.prenom} {user.nom}
        </div>
      </div>

      {/* Statistiques globales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{agents.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Services</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{services.length}</div>
          </CardContent>
        </Card>
      </div>

      {/* Onglets */}
      <Tabs defaultValue="agents" className="space-y-4">
        <TabsList>
          <TabsTrigger value="agents">Agents</TabsTrigger>
          <TabsTrigger value="services">Services</TabsTrigger>
        </TabsList>

        <TabsContent value="agents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Liste des Agents</CardTitle>
              <CardDescription>
                Gestion des agents et de leurs informations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Nom</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Rôle</TableHead>
                    <TableHead>Service</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {agents.map((agent) => (
                    <TableRow key={agent.id}>
                      <TableCell className="font-medium">
                        {agent.prenom} {agent.nom}
                      </TableCell>
                      <TableCell>{agent.email}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{agent.role}</Badge>
                      </TableCell>
                      <TableCell>
                        {services.find(s => s.id === agent.service_id)?.nom_service || 'N/A'}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => onViewAgent(agent.id)}
                        >
                          Voir
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="services" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Liste des Services</CardTitle>
              <CardDescription>
                Gestion des services et de leurs responsables
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Nom du Service</TableHead>
                    <TableHead>Responsable</TableHead>
                    <TableHead>Nombre d'Agents</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {services.map((service) => (
                    <TableRow key={service.id}>
                      <TableCell className="font-medium">
                        {service.nom_service}
                      </TableCell>
                      <TableCell>
                        {service.responsable ? 
                          `${service.responsable.prenom} ${service.responsable.nom}` : 
                          'Non assigné'
                        }
                      </TableCell>
                      <TableCell>{service.nb_agents || 0}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AdminDashboardSimple


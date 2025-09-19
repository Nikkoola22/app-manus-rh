import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Users, Building, Clock, Plus, Edit, Trash2, Eye, Stethoscope } from 'lucide-react'
import api from '../services/api'

const AdminDashboard = ({ user, onViewAgent }) => {
  const [agents, setAgents] = useState([])
  const [services, setServices] = useState([])
  const [demandes, setDemandes] = useState([])
  const [arretsMaladie, setArretsMaladie] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAgentForm, setShowAgentForm] = useState(false)
  const [showServiceForm, setShowServiceForm] = useState(false)
  const [showArretMaladieForm, setShowArretMaladieForm] = useState(false)
  const [editingAgent, setEditingAgent] = useState(null)
  const [editingService, setEditingService] = useState(null)
  const [editingArretMaladie, setEditingArretMaladie] = useState(null)

  const [agentForm, setAgentForm] = useState({
    nom: '',
    prenom: '',
    email: '',
    password: '',
    role: 'Agent',
    service_id: '',
    quotite_travail: 35,
    date_debut_contrat: '',
    annee_entree_fp: '',
    date_fin_contrat: '',
    solde_ca: 0,
    solde_rtt: 0,
    solde_cet: 0,
    solde_bonifications: 0,
    solde_jours_sujetions: 0,
    solde_conges_formations: 0,
    solde_hs: 0
  })

  const [serviceForm, setServiceForm] = useState({
    nom_service: '',
    responsable_id: ''
  })

  const [arretMaladieForm, setArretMaladieForm] = useState({
    agent_id: '',
    date_debut: '',
    date_fin: '',
    motif: ''
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    console.log('🔍 AdminDashboard: fetchData démarré')
    try {
      const [agentsResponse, servicesResponse, demandesResponse, arretsMaladieResponse] = await Promise.all([
        api.getAgents(),
        api.getServices(),
        api.getDemandes(),
        api.getArretsMaladie()
      ])
      console.log('🔍 AdminDashboard: Réponses reçues', { agentsResponse, servicesResponse, demandesResponse, arretsMaladieResponse })

      if (agentsResponse.ok) {
        const agentsData = await agentsResponse.json()
        setAgents(agentsData)
      }

      if (servicesResponse.ok) {
        const servicesData = await servicesResponse.json()
        setServices(servicesData)
      }

      if (demandesResponse.ok) {
        const demandesData = await demandesResponse.json()
        setDemandes(demandesData)
      }

      if (arretsMaladieResponse.ok) {
        const arretsMaladieData = await arretsMaladieResponse.json()
        setArretsMaladie(arretsMaladieData)
      }
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err)
    } finally {
      console.log('🔍 AdminDashboard: fetchData terminé, setLoading(false)')
      setLoading(false)
    }
  }

  const formatHours = (hours) => `${hours}h`
  const formatDate = (dateString) => new Date(dateString).toLocaleDateString('fr-FR')

  const getStatusColor = (status) => {
    switch (status) {
      case 'Approuvée':
        return 'bg-green-100 text-green-800'
      case 'Refusée':
        return 'bg-red-100 text-red-800'
      case 'En attente':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getRoleColor = (role) => {
    switch (role) {
      case 'Admin':
        return 'bg-red-100 text-red-800'
      case 'Responsable':
        return 'bg-blue-100 text-blue-800'
      case 'Agent':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  // Fonctions de gestion des formulaires
  const handleAgentSubmit = async (e) => {
    e.preventDefault()
    try {
      const result = await api.createAgent(agentForm)
      if (result.success) {
        setAgents([...agents, result.agent])
        setShowAgentForm(false)
        setAgentForm({
          nom: '',
          prenom: '',
          email: '',
          password: '',
          role: 'Agent',
          service_id: '',
          quotite_travail: 35,
          date_debut_contrat: '',
          annee_entree_fp: '',
          date_fin_contrat: '',
          solde_ca: 0,
          solde_rtt: 0,
          solde_cet: 0,
          solde_bonifications: 0,
          solde_jours_sujetions: 0,
          solde_conges_formations: 0,
          solde_hs: 0
        })
        alert('Agent créé avec succès !')
      }
    } catch (error) {
      console.error('Erreur lors de la création de l\'agent:', error)
      alert('Erreur lors de la création de l\'agent')
    }
  }

  const handleServiceSubmit = async (e) => {
    e.preventDefault()
    try {
      const result = await api.createService(serviceForm)
      if (result.success) {
        setServices([...services, result.service])
        setShowServiceForm(false)
        setServiceForm({
          nom_service: '',
          responsable_id: ''
        })
        alert('Service créé avec succès !')
      }
    } catch (error) {
      console.error('Erreur lors de la création du service:', error)
      alert('Erreur lors de la création du service')
    }
  }

  const handleArretMaladieSubmit = async (e) => {
    e.preventDefault()
    try {
      // Simulation de création d'arrêt maladie
      const newArret = {
        id: Date.now(),
        agent_id: arretMaladieForm.agent_id,
        date_debut: arretMaladieForm.date_debut,
        date_fin: arretMaladieForm.date_fin,
        motif: arretMaladieForm.motif,
        statut: 'En cours',
        agent: {
          prenom: agents.find(a => a.id === parseInt(arretMaladieForm.agent_id))?.prenom || 'Agent',
          nom: agents.find(a => a.id === parseInt(arretMaladieForm.agent_id))?.nom || 'Inconnu'
        }
      }
      setArretsMaladie([...arretsMaladie, newArret])
      setShowArretMaladieForm(false)
      setArretMaladieForm({
        agent_id: '',
        date_debut: '',
        date_fin: '',
        motif: ''
      })
      alert('Arrêt maladie créé avec succès !')
    } catch (error) {
      console.error('Erreur lors de la création de l\'arrêt maladie:', error)
      alert('Erreur lors de la création de l\'arrêt maladie')
    }
  }

  const demandesEnAttente = demandes.filter(d => d.statut === 'En attente')
  const totalAgents = agents.length
  const totalServices = services.length

  console.log('🔍 AdminDashboard: Render - loading:', loading, 'agents:', agents.length, 'services:', services.length)
  
  return (
    <div className="space-y-6">
      {/* Statistiques globales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalAgents}</div>
            <p className="text-xs text-muted-foreground">Dans tous les services</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Services</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalServices}</div>
            <p className="text-xs text-muted-foreground">Services actifs</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Demandes en attente</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{demandesEnAttente.length}</div>
            <p className="text-xs text-muted-foreground">À traiter</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total demandes</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{demandes.length}</div>
            <p className="text-xs text-muted-foreground">Toutes demandes</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="agents" className="space-y-4">
        <TabsList>
          <TabsTrigger value="agents">Agents ({totalAgents})</TabsTrigger>
          <TabsTrigger value="services">Services ({totalServices})</TabsTrigger>
          <TabsTrigger value="demandes">Demandes ({demandes.length})</TabsTrigger>
          <TabsTrigger value="arrets-maladie">Arrêts maladie ({arretsMaladie.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="agents">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Gestion des agents</CardTitle>
                  <CardDescription>
                    Créer, modifier et supprimer les comptes agents
                  </CardDescription>
                </div>
                <Button onClick={() => setShowAgentForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouvel agent
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-4">Chargement...</div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Rôle</TableHead>
                      <TableHead>Service</TableHead>
                      <TableHead>CA</TableHead>
                      <TableHead>RTT</TableHead>
                      <TableHead>HS</TableHead>
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
                          <Badge className={getRoleColor(agent.role)}>
                            {agent.role}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {services.find(s => s.id === agent.service_id)?.nom_service || '-'}
                        </TableCell>
                        <TableCell>{formatHours(agent.solde_ca || 0)}</TableCell>
                        <TableCell>{formatHours(agent.solde_rtt || 0)}</TableCell>
                        <TableCell>{formatHours(agent.solde_hs || 0)}</TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => onViewAgent && onViewAgent(agent.id)}
                              title="Voir le profil"
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setEditingAgent(agent)}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleDeleteAgent(agent.id)}
                              disabled={agent.id === user.id}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="services">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Gestion des services</CardTitle>
                  <CardDescription>
                    Créer, modifier et supprimer les services
                  </CardDescription>
                </div>
                <Button onClick={() => setShowServiceForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouveau service
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-4">Chargement...</div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Service</TableHead>
                      <TableHead>Responsable</TableHead>
                      <TableHead>Nb agents</TableHead>
                      <TableHead>Actions</TableHead>
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
                            'Aucun'
                          }
                        </TableCell>
                        <TableCell>{service.nb_agents || 0}</TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setEditingService(service)}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleDeleteService(service.id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="demandes">
          <Card>
            <CardHeader>
              <CardTitle>Toutes les demandes</CardTitle>
              <CardDescription>
                Vue d'ensemble de toutes les demandes de congés
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-4">Chargement...</div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Service</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>Statut</TableHead>
                      <TableHead>Date demande</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {demandes.map((demande) => (
                      <TableRow key={demande.id}>
                        <TableCell className="font-medium">
                          {demande.agent?.prenom} {demande.agent?.nom}
                        </TableCell>
                        <TableCell>
                          {services.find(s => s.id === demande.agent?.service_id)?.nom_service || '-'}
                        </TableCell>
                        <TableCell>{demande.type_absence}</TableCell>
                        <TableCell>
                          {formatDate(demande.date_debut)} - {formatDate(demande.date_fin)}
                        </TableCell>
                        <TableCell>{formatHours(demande.nb_heures)}</TableCell>
                        <TableCell>
                          <Badge className={getStatusColor(demande.statut)}>
                            {demande.statut}
                          </Badge>
                        </TableCell>
                        <TableCell>{formatDate(demande.date_demande)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="arrets-maladie">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Gestion des arrêts maladie</CardTitle>
                  <CardDescription>
                    Enregistrer et gérer les arrêts maladie des agents
                  </CardDescription>
                </div>
                <Button onClick={() => setShowArretMaladieForm(true)}>
                  <Stethoscope className="h-4 w-4 mr-2" />
                  Nouvel arrêt maladie
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-4">Chargement...</div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Service</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>RTT perdus</TableHead>
                      <TableHead>Créé par</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {arretsMaladie.map((arret) => (
                      <TableRow key={arret.id}>
                        <TableCell className="font-medium">
                          {arret.agent_nom}
                        </TableCell>
                        <TableCell>
                          {services.find(s => s.id === agents.find(a => a.id === arret.agent_id)?.service_id)?.nom_service || '-'}
                        </TableCell>
                        <TableCell>
                          {formatDate(arret.date_debut)} - {formatDate(arret.date_fin)}
                        </TableCell>
                        <TableCell>{arret.nb_jours} jours</TableCell>
                        <TableCell>
                          {arret.perte_rtt > 0 ? (
                            <Badge variant="destructive">{arret.perte_rtt} jour(s)</Badge>
                          ) : (
                            <span className="text-gray-500">0</span>
                          )}
                        </TableCell>
                        <TableCell>{arret.createur_nom}</TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setEditingArretMaladie(arret)}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleDeleteArretMaladie(arret.id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AdminDashboard
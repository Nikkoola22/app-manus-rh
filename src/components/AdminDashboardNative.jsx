import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Users, Building, Clock, Plus, Edit, Trash2, Eye, Stethoscope, ArrowLeft, User, Mail, Calendar } from 'lucide-react'

const AdminDashboardNative = ({ user, onViewAgent }) => {
  const [agents, setAgents] = useState([])
  const [services, setServices] = useState([])
  const [demandes, setDemandes] = useState([])
  const [arretsMaladie, setArretsMaladie] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAgentForm, setShowAgentForm] = useState(false)
  const [editingAgent, setEditingAgent] = useState(null)
  const [editingService, setEditingService] = useState(null)
  const [selectedService, setSelectedService] = useState(null)

  // Form states
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

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    console.log('🔍 AdminDashboardNative: fetchData démarré')
    try {
      const [agentsResponse, servicesResponse, demandesResponse, arretsMaladieResponse] = await Promise.all([
        fetch('/api/agents', { credentials: 'include' }),
        fetch('/api/services', { credentials: 'include' }),
        fetch('/api/demandes', { credentials: 'include' }),
        fetch('/api/arret-maladie', { credentials: 'include' })
      ])

      if (agentsResponse.ok) {
        const agentsData = await agentsResponse.json()
        setAgents(agentsData)
      }

      if (servicesResponse.ok) {
        const servicesData = await servicesResponse.json()
        console.log('🔍 Services chargés:', servicesData)
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
      console.log('🔍 AdminDashboardNative: setLoading(false)')
      setLoading(false)
    }
  }

  const demandesEnAttente = demandes.filter(d => d.statut === 'En attente')
  const totalAgents = agents.length
  const totalServices = services.length

  // Fonction pour mettre à jour le service d'un agent
  const updateAgentService = async (agentId, newServiceId) => {
    try {
      const response = await fetch(`/api/agents/${agentId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ service_id: parseInt(newServiceId) })
      })
      
      if (response.ok) {
        // Mettre à jour l'agent dans la liste locale
        setAgents(prevAgents => 
          prevAgents.map(agent => 
            agent.id === agentId 
              ? { ...agent, service_id: parseInt(newServiceId) }
              : agent
          )
        )
        setEditingService(null)
        console.log('Service mis à jour avec succès')
      } else {
        alert('Erreur lors de la mise à jour du service')
      }
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de la mise à jour du service')
    }
  }

  // Fonction pour supprimer un agent
  const deleteAgent = async (agentId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet agent ? Cette action est irréversible.')) {
      return
    }

    try {
      const response = await fetch(`/api/agents/${agentId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      })

      if (response.ok) {
        // Supprimer l'agent de la liste locale
        setAgents(prevAgents => prevAgents.filter(agent => agent.id !== agentId))
        console.log('Agent supprimé avec succès')
      } else {
        const errorData = await response.json()
        console.error('Erreur lors de la suppression de l\'agent:', errorData.error)
        alert(`Erreur lors de la suppression: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Erreur lors de la suppression de l\'agent:', error)
      alert('Erreur lors de la suppression de l\'agent')
    }
  }

  // Fonction pour supprimer un service
  const deleteService = async (serviceId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce service ? Cette action est irréversible et supprimera tous les agents associés.')) {
      return
    }

    try {
      const response = await fetch(`/api/services/${serviceId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      })

      if (response.ok) {
        // Supprimer le service de la liste locale
        setServices(prevServices => prevServices.filter(service => service.id !== serviceId))
        // Supprimer aussi les agents de ce service
        setAgents(prevAgents => prevAgents.filter(agent => agent.service_id !== serviceId))
        console.log('Service supprimé avec succès')
      } else {
        const errorData = await response.json()
        console.error('Erreur lors de la suppression du service:', errorData.error)
        alert(`Erreur lors de la suppression: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Erreur lors de la suppression du service:', error)
      alert('Erreur lors de la suppression du service')
    }
  }

  // Fonction pour gérer la sélection d'un service
  const handleServiceSelect = (service) => {
    setSelectedService(service)
  }

  // Fonction pour retourner à la liste des services
  const handleBackToServices = () => {
    setSelectedService(null)
  }

  console.log('🔍 AdminDashboardNative: Render - loading:', loading, 'agents:', agents.length, 'services:', services.length)

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Tableau de Bord Admin</h1>
        <div className="bg-blue-100 p-4 rounded">
          <p>Chargement des données en cours...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tableau de Bord Admin (Version Native)</h1>
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
            <div className="text-2xl font-bold">{totalAgents}</div>
            <p className="text-xs text-muted-foreground">Dans tous les services</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Services</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalServices}</div>
            <p className="text-xs text-muted-foreground">Services actifs</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Demandes en Attente</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{demandesEnAttente.length}</div>
            <p className="text-xs text-muted-foreground">À traiter</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Arrêts Maladie</CardTitle>
            <Stethoscope className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{arretsMaladie.length}</div>
            <p className="text-xs text-muted-foreground">Enregistrés</p>
          </CardContent>
        </Card>
      </div>

      {/* Onglets principaux */}
      <Tabs defaultValue="agents" className="space-y-4">
        <TabsList>
          <TabsTrigger value="agents">Agents</TabsTrigger>
          <TabsTrigger value="services">Services</TabsTrigger>
          <TabsTrigger value="demandes">Demandes</TabsTrigger>
          <TabsTrigger value="arrets-maladie">Arrêts Maladie</TabsTrigger>
        </TabsList>

        {/* Onglet Agents */}
        <TabsContent value="agents" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Gestion des Agents</CardTitle>
                  <CardDescription>
                    Créer, modifier et gérer les agents
                  </CardDescription>
                </div>
                <Button onClick={() => setShowAgentForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouvel Agent
                </Button>
              </div>
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
                        {editingService === agent.id ? (
                          <div className="flex items-center space-x-2">
                            <select
                              className="p-1 border border-gray-300 rounded text-sm"
                              value={agent.service_id || ''}
                              onChange={(e) => updateAgentService(agent.id, e.target.value)}
                              onBlur={() => setEditingService(null)}
                              autoFocus
                            >
                              <option value="">Sélectionner un service</option>
                              {services.map(service => (
                                <option key={service.id} value={service.id}>
                                  {service.nom_service}
                                </option>
                              ))}
                            </select>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => setEditingService(null)}
                              className="text-xs px-2 py-1"
                            >
                              Annuler
                            </Button>
                          </div>
                        ) : (
                          <div 
                            className="cursor-pointer hover:bg-gray-100 p-1 rounded flex items-center justify-between"
                            onClick={() => setEditingService(agent.id)}
                            title="Cliquer pour changer le service"
                          >
                            <span>{services.find(s => s.id === agent.service_id)?.nom_service || 'Non assigné'}</span>
                            <Edit className="h-3 w-3 ml-1 text-gray-400" />
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex space-x-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              console.log('Clic sur Voir pour agent:', agent.id)
                              onViewAgent(agent.id)
                            }}
                            title="Voir la fiche de l'agent"
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              console.log('Clic sur Modifier pour agent:', agent.id)
                              setEditingAgent(agent)
                              setAgentForm({
                                nom: agent.nom || '',
                                prenom: agent.prenom || '',
                                email: agent.email || '',
                                password: '',
                                role: agent.role || 'Agent',
                                service_id: agent.service_id ? agent.service_id.toString() : '',
                                quotite_travail: agent.quotite_travail || 35,
                                date_debut_contrat: agent.date_debut_contrat || '',
                                annee_entree_fp: agent.annee_entree_fp || '',
                                date_fin_contrat: agent.date_fin_contrat || '',
                                solde_ca: agent.solde_ca || 0,
                                solde_rtt: agent.solde_rtt || 0,
                                solde_cet: agent.solde_cet || 0,
                                solde_bonifications: agent.solde_bonifications || 0,
                                solde_jours_sujetions: agent.solde_jours_sujetions || 0,
                                solde_conges_formations: agent.solde_conges_formations || 0,
                                solde_hs: agent.solde_hs || 0
                              })
                              setShowAgentForm(true)
                            }}
                            title="Modifier l'agent"
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              console.log('Clic sur Supprimer pour agent:', agent.id)
                              deleteAgent(agent.id)
                            }}
                            className="text-red-600 hover:text-red-700 hover:bg-red-50"
                            title="Supprimer l'agent"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet Services */}
        <TabsContent value="services" className="space-y-4">
          {!selectedService ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Gestion des Services</CardTitle>
                    <CardDescription>
                      Créer et gérer les services
                    </CardDescription>
                  </div>
                  <Button onClick={() => {/* TODO: Ajouter création de service */}}>
                    <Plus className="h-4 w-4 mr-2" />
                    Nouveau Service
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nom du Service</TableHead>
                      <TableHead>Responsable</TableHead>
                      <TableHead>Nombre d'Agents</TableHead>
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
                          {service.responsable ? (
                            <div>
                              <div>{`${service.responsable.prenom || ''} ${service.responsable.nom || ''}`.trim()}</div>
                              <div className="text-xs text-gray-500">
                                ID: {service.responsable.id} | Rôle: {service.responsable.role}
                              </div>
                            </div>
                          ) : (
                            'Non assigné'
                          )}
                        </TableCell>
                        <TableCell>{service.nb_agents || 0}</TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => handleServiceSelect(service)}
                              className="flex items-center space-x-2"
                            >
                              <Building className="h-4 w-4" />
                              <span>Gérer</span>
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => deleteService(service.id)}
                              className="text-red-600 hover:text-red-700 hover:bg-red-50"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          ) : (
            <ServiceDetailView 
              service={selectedService} 
              agents={agents.filter(agent => agent.service_id === selectedService.id)}
              onBack={handleBackToServices}
              onViewAgent={onViewAgent}
              onDeleteAgent={deleteAgent}
            />
          )}
        </TabsContent>

        {/* Onglet Demandes */}
        <TabsContent value="demandes" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Demandes de Congé</CardTitle>
              <CardDescription>
                Gérer les demandes de congé des agents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Agent</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Période</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {demandes.map((demande) => {
                    const agent = agents.find(a => a.id === demande.agent_id)
                    return (
                      <TableRow key={demande.id}>
                        <TableCell className="font-medium">
                          {agent ? `${agent.prenom} ${agent.nom}` : 'N/A'}
                        </TableCell>
                        <TableCell>{demande.type_absence}</TableCell>
                        <TableCell>
                          {new Date(demande.date_debut).toLocaleDateString()} - {new Date(demande.date_fin).toLocaleDateString()}
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">{demande.statut}</Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => {
                                console.log('Voir demande:', demande.id, 'Agent:', demande.agent_id)
                                // Rediriger vers la fiche de l'agent qui a fait la demande
                                if (onViewAgent) {
                                  onViewAgent(demande.agent_id)
                                }
                              }}
                              title={`Voir la fiche de ${agent ? `${agent.prenom} ${agent.nom}` : 'l\'agent'}`}
                            >
                              Voir Agent
                            </Button>
                            {demande.statut === 'En attente' && (
                              <>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  className="bg-green-100 text-green-800 hover:bg-green-200"
                                  onClick={async () => {
                                    try {
                                      const response = await fetch(`/api/demandes/${demande.id}/valider`, {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        credentials: 'include',
                                        body: JSON.stringify({ action: 'approuver', commentaires: 'Demande approuvée par l\'admin' })
                                      })
                                      if (response.ok) {
                                        await fetchData() // Recharger les données
                                        console.log('Demande approuvée')
                                      } else {
                                        alert('Erreur lors de l\'approbation')
                                      }
                                    } catch (error) {
                                      console.error('Erreur:', error)
                                      alert('Erreur lors de l\'approbation')
                                    }
                                  }}
                                >
                                  Approuver
                                </Button>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  className="bg-red-100 text-red-800 hover:bg-red-200"
                                  onClick={async () => {
                                    try {
                                      const response = await fetch(`/api/demandes/${demande.id}/valider`, {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        credentials: 'include',
                                        body: JSON.stringify({ action: 'refuser', commentaires: 'Demande refusée par l\'admin' })
                                      })
                                      if (response.ok) {
                                        await fetchData() // Recharger les données
                                        console.log('Demande refusée')
                                      } else {
                                        alert('Erreur lors du refus')
                                      }
                                    } catch (error) {
                                      console.error('Erreur:', error)
                                      alert('Erreur lors du refus')
                                    }
                                  }}
                                >
                                  Refuser
                                </Button>
                              </>
                            )}
                            {(demande.statut === 'Approuvée' || demande.statut === 'Refusée') && (
                              <span className="text-sm text-gray-500">
                                {demande.statut === 'Approuvée' ? '✅ Traitée' : '❌ Refusée'}
                              </span>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet Arrêts Maladie */}
        <TabsContent value="arrets-maladie" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Arrêts Maladie</CardTitle>
                  <CardDescription>
                    Gérer les arrêts maladie des agents
                  </CardDescription>
                </div>
                <Button onClick={() => {/* TODO: Ajouter création d'arrêt maladie */}}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouvel Arrêt
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Agent</TableHead>
                    <TableHead>Période</TableHead>
                    <TableHead>Motif</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {arretsMaladie.map((arret) => {
                    const agent = agents.find(a => a.id === arret.agent_id)
                    return (
                      <TableRow key={arret.id}>
                        <TableCell className="font-medium">
                          {agent ? `${agent.prenom} ${agent.nom}` : 'N/A'}
                        </TableCell>
                        <TableCell>
                          {new Date(arret.date_debut).toLocaleDateString()} - {new Date(arret.date_fin).toLocaleDateString()}
                        </TableCell>
                        <TableCell>{arret.motif}</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">
                            Voir
                          </Button>
                        </TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Formulaire de modification d'agent avec selects HTML natifs */}
      <Dialog open={showAgentForm} onOpenChange={setShowAgentForm}>
        <DialogContent className="max-w-2xl max-h-[90vh] bg-white border border-gray-200 shadow-xl overflow-hidden flex flex-col z-50">
          <DialogHeader className="flex-shrink-0">
            <DialogTitle className="text-lg font-semibold text-gray-900">
              {editingAgent ? 'Modifier l\'agent' : 'Nouvel agent'}
            </DialogTitle>
            <DialogDescription className="text-sm text-gray-600">
              {editingAgent ? 'Modifiez les informations de l\'agent' : 'Créez un nouveau compte agent'}
            </DialogDescription>
          </DialogHeader>
          <div className="flex-1 overflow-y-auto px-1">
            <form id="agent-form" onSubmit={async (e) => {
              e.preventDefault()
              try {
                const url = editingAgent ? `/api/agents/${editingAgent.id}` : '/api/agents'
                const method = editingAgent ? 'PUT' : 'POST'
                
                const response = await fetch(url, {
                  method,
                  headers: { 'Content-Type': 'application/json' },
                  credentials: 'include',
                  body: JSON.stringify(agentForm)
                })
                
                if (response.ok) {
                  await fetchData() // Recharger les données
                  setShowAgentForm(false)
                  setEditingAgent(null)
                  setAgentForm({
                    nom: '', prenom: '', email: '', password: '', role: 'Agent',
                    service_id: '', quotite_travail: 35, date_debut_contrat: '',
                    annee_entree_fp: '', date_fin_contrat: '', solde_ca: 0,
                    solde_rtt: 0, solde_cet: 0, solde_bonifications: 0,
                    solde_jours_sujetions: 0, solde_conges_formations: 0, solde_hs: 0
                  })
                } else {
                  alert('Erreur lors de la sauvegarde')
                }
              } catch (error) {
                console.error('Erreur:', error)
                alert('Erreur lors de la sauvegarde')
              }
            }} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="prenom" className="dialog-label">Prénom</Label>
                  <Input
                    id="prenom"
                    className="dialog-input"
                    value={agentForm.prenom}
                    onChange={(e) => setAgentForm({...agentForm, prenom: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="nom" className="dialog-label">Nom</Label>
                  <Input
                    id="nom"
                    className="dialog-input"
                    value={agentForm.nom}
                    onChange={(e) => setAgentForm({...agentForm, nom: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="email" className="dialog-label">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    className="dialog-input"
                    value={agentForm.email}
                    onChange={(e) => setAgentForm({...agentForm, email: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="password" className="dialog-label">Mot de passe</Label>
                  <Input
                    id="password"
                    type="password"
                    className="dialog-input"
                    value={agentForm.password}
                    onChange={(e) => setAgentForm({...agentForm, password: e.target.value})}
                    placeholder={editingAgent ? "Laisser vide pour ne pas changer" : ""}
                    required={!editingAgent}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="role" className="dialog-label">Rôle</Label>
                  <select
                    id="role"
                    className="w-full p-2 border border-gray-300 rounded-md bg-white text-gray-900"
                    value={agentForm.role}
                    onChange={(e) => {
                      console.log('Rôle sélectionné (HTML):', e.target.value)
                      setAgentForm({...agentForm, role: e.target.value})
                    }}
                  >
                    <option value="Agent">Agent</option>
                    <option value="Responsable">Responsable</option>
                    <option value="Admin">Admin</option>
                  </select>
                </div>
                <div>
                  <Label htmlFor="service_id" className="dialog-label">Service</Label>
                  <select
                    id="service_id"
                    className="w-full p-2 border border-gray-300 rounded-md bg-white text-gray-900"
                    value={agentForm.service_id}
                    onChange={(e) => {
                      console.log('Service sélectionné (HTML):', e.target.value)
                      setAgentForm({...agentForm, service_id: e.target.value})
                    }}
                  >
                    <option value="">Sélectionner un service</option>
                    {services.map(service => (
                      <option key={service.id} value={service.id.toString()}>
                        {service.nom_service}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="quotite_travail" className="dialog-label">Quotité de travail (h/semaine)</Label>
                  <Input
                    id="quotite_travail"
                    type="number"
                    className="dialog-input"
                    value={agentForm.quotite_travail}
                    onChange={(e) => setAgentForm({...agentForm, quotite_travail: parseFloat(e.target.value) || 35})}
                    min="1"
                    max="40"
                  />
                </div>
                <div>
                  <Label htmlFor="date_debut_contrat" className="dialog-label">Date de début de contrat</Label>
                  <Input
                    id="date_debut_contrat"
                    type="date"
                    className="dialog-input"
                    value={agentForm.date_debut_contrat}
                    onChange={(e) => setAgentForm({...agentForm, date_debut_contrat: e.target.value})}
                  />
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Soldes initiaux</h3>
                
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="solde_ca" className="dialog-label">Solde CA (jours)</Label>
                    <Input
                      id="solde_ca"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_ca}
                      onChange={(e) => setAgentForm({...agentForm, solde_ca: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                  <div>
                    <Label htmlFor="solde_rtt" className="dialog-label">Solde RTT (jours)</Label>
                    <Input
                      id="solde_rtt"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_rtt}
                      onChange={(e) => setAgentForm({...agentForm, solde_rtt: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                  <div>
                    <Label htmlFor="solde_cet" className="dialog-label">Solde CET (jours)</Label>
                    <Input
                      id="solde_cet"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_cet}
                      onChange={(e) => setAgentForm({...agentForm, solde_cet: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="solde_hs" className="dialog-label">Solde HS (jours)</Label>
                    <Input
                      id="solde_hs"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_hs}
                      onChange={(e) => setAgentForm({...agentForm, solde_hs: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                  <div>
                    <Label htmlFor="solde_bonifications" className="dialog-label">Solde Bonifications (jours)</Label>
                    <Input
                      id="solde_bonifications"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_bonifications}
                      onChange={(e) => setAgentForm({...agentForm, solde_bonifications: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                  <div>
                    <Label htmlFor="solde_jours_sujetions" className="dialog-label">Solde Jours de sujétions (jours)</Label>
                    <Input
                      id="solde_jours_sujetions"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_jours_sujetions}
                      onChange={(e) => setAgentForm({...agentForm, solde_jours_sujetions: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="solde_conges_formations" className="dialog-label">Solde Congés formations (jours)</Label>
                    <Input
                      id="solde_conges_formations"
                      type="number"
                      className="dialog-input"
                      value={agentForm.solde_conges_formations}
                      onChange={(e) => setAgentForm({...agentForm, solde_conges_formations: parseFloat(e.target.value) || 0})}
                      min="0"
                      step="0.5"
                    />
                  </div>
                  <div></div>
                  <div></div>
                </div>
              </div>
            </form>
          </div>
          <div className="flex-shrink-0 flex justify-end space-x-2 pt-4 border-t border-gray-200">
            <Button 
              type="button" 
              variant="outline" 
              className="dialog-button-outline"
              onClick={() => {
                setShowAgentForm(false)
                setEditingAgent(null)
                setAgentForm({
                  nom: '', prenom: '', email: '', password: '', role: 'Agent',
                  service_id: '', quotite_travail: 35, date_debut_contrat: '',
                  annee_entree_fp: '', date_fin_contrat: '', solde_ca: 0,
                  solde_rtt: 0, solde_cet: 0, solde_bonifications: 0,
                  solde_jours_sujetions: 0, solde_conges_formations: 0, solde_hs: 0
                })
              }}
            >
              Annuler
            </Button>
            <Button type="submit" form="agent-form" className="dialog-button">
              {editingAgent ? 'Modifier' : 'Créer'}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}

// Composant pour afficher les détails d'un service
const ServiceDetailView = ({ service, agents, onBack, onViewAgent, onDeleteAgent }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('fr-FR')
  }

  const formatHours = (hours) => {
    if (!hours) return '0h'
    return `${hours}h`
  }

  return (
    <div className="space-y-6">
      {/* Header avec bouton retour */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button onClick={onBack} variant="outline" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Retour aux Services
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{service.nom_service}</h1>
            <p className="text-gray-600">Gestion du service</p>
          </div>
        </div>
      </div>

      {/* Informations du service */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Responsable du service */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <User className="h-5 w-5 mr-2" />
              Responsable du Service
            </CardTitle>
          </CardHeader>
          <CardContent>
            {service.responsable ? (
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-500">Nom complet</label>
                  <p className="text-sm font-semibold">
                    {service.responsable.prenom} {service.responsable.nom}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Email</label>
                  <p className="text-sm">{service.responsable.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Rôle</label>
                  <p className="text-sm">
                    <Badge variant="outline">{service.responsable.role}</Badge>
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Quotité de travail</label>
                  <p className="text-sm">{service.responsable.quotite_travail}h/semaine</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Date d'entrée</label>
                  <p className="text-sm">{formatDate(service.responsable.date_debut_contrat)}</p>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">Aucun responsable assigné</p>
                <Button variant="outline" size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Assigner un responsable
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Statistiques du service */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Building className="h-5 w-5 mr-2" />
              Statistiques du Service
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Nombre d'agents</span>
                <span className="text-2xl font-bold text-blue-600">{agents.length}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Responsable assigné</span>
                <span className="text-sm">
                  {service.responsable ? (
                    <Badge className="bg-green-100 text-green-800">Oui</Badge>
                  ) : (
                    <Badge variant="destructive">Non</Badge>
                  )}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Date de création</span>
                <span className="text-sm">{formatDate(service.date_creation)}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Liste des agents du service */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="h-5 w-5 mr-2" />
            Agents du Service ({agents.length})
          </CardTitle>
          <CardDescription>
            Liste de tous les agents assignés à ce service
          </CardDescription>
        </CardHeader>
        <CardContent>
          {agents.length === 0 ? (
            <div className="text-center py-8">
              <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Aucun agent assigné à ce service</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nom</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Rôle</TableHead>
                  <TableHead>Quotité</TableHead>
                  <TableHead>Date d'entrée</TableHead>
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
                    <TableCell>{agent.quotite_travail}h/semaine</TableCell>
                    <TableCell>{formatDate(agent.date_debut_contrat)}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            console.log('Voir agent depuis service:', agent.id)
                            if (onViewAgent) {
                              onViewAgent(agent.id)
                            }
                          }}
                        >
                          <Eye className="h-4 w-4 mr-2" />
                          Voir
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => onDeleteAgent && onDeleteAgent(agent.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
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
    </div>
  )
}

export default AdminDashboardNative

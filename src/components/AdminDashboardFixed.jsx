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

const AdminDashboardFixed = ({ user, onViewAgent }) => {
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

  const [serviceForm, setServiceForm] = useState({
    nom_service: '',
    description: '',
    responsable_id: ''
  })

  const [arretMaladieForm, setArretMaladieForm] = useState({
    agent_id: '',
    date_debut: '',
    date_fin: '',
    motif: '',
    nb_jours: 0
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    console.log('🔍 AdminDashboardFixed: fetchData démarré')
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
      console.log('🔍 AdminDashboardFixed: setLoading(false)')
      setLoading(false)
    }
  }

  const demandesEnAttente = demandes.filter(d => d.statut === 'En attente')
  const totalAgents = agents.length
  const totalServices = services.length

  console.log('🔍 AdminDashboardFixed: Render - loading:', loading, 'agents:', agents.length, 'services:', services.length)

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
                        {services.find(s => s.id === agent.service_id)?.nom_service || 'N/A'}
                      </TableCell>
                      <TableCell>
                        <div className="flex space-x-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => onViewAgent(agent.id)}
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
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
                          >
                            <Edit className="h-4 w-4" />
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
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Gestion des Services</CardTitle>
                  <CardDescription>
                    Créer et gérer les services
                  </CardDescription>
                </div>
                <Button onClick={() => setShowServiceForm(true)}>
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
                        {service.responsable ? 
                          `${service.responsable.prenom} ${service.responsable.nom}` : 
                          'Non assigné'
                        }
                      </TableCell>
                      <TableCell>{service.nb_agents || 0}</TableCell>
                      <TableCell>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setEditingService(service)
                            setServiceForm({
                              nom_service: service.nom_service || '',
                              description: service.description || '',
                              responsable_id: service.responsable_id ? service.responsable_id.toString() : ''
                            })
                            setShowServiceForm(true)
                          }}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
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
                <Button onClick={() => setShowArretMaladieForm(true)}>
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

      {/* Formulaire de modification d'agent */}
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
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={agentForm.email}
                    onChange={(e) => setAgentForm({...agentForm, email: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="password">Mot de passe</Label>
                  <Input
                    id="password"
                    type="password"
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
                  <Select 
                    value={agentForm.role} 
                    onValueChange={(value) => {
                      console.log('Rôle sélectionné:', value)
                      setAgentForm({...agentForm, role: value})
                    }}
                  >
                    <SelectTrigger className="dialog-input">
                      <SelectValue placeholder="Sélectionner un rôle" />
                    </SelectTrigger>
                    <SelectContent className="z-[9999] bg-white border border-gray-200 shadow-xl">
                      <SelectItem 
                        value="Agent" 
                        className="cursor-pointer hover:bg-gray-100 px-3 py-2"
                        onClick={() => console.log('Agent cliqué')}
                      >
                        Agent
                      </SelectItem>
                      <SelectItem 
                        value="Responsable" 
                        className="cursor-pointer hover:bg-gray-100 px-3 py-2"
                        onClick={() => console.log('Responsable cliqué')}
                      >
                        Responsable
                      </SelectItem>
                      <SelectItem 
                        value="Admin" 
                        className="cursor-pointer hover:bg-gray-100 px-3 py-2"
                        onClick={() => console.log('Admin cliqué')}
                      >
                        Admin
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="service_id" className="dialog-label">Service</Label>
                  <Select 
                    value={agentForm.service_id} 
                    onValueChange={(value) => {
                      console.log('Service sélectionné:', value)
                      setAgentForm({...agentForm, service_id: value})
                    }}
                  >
                    <SelectTrigger className="dialog-input">
                      <SelectValue placeholder="Sélectionner un service" />
                    </SelectTrigger>
                    <SelectContent className="z-[9999] bg-white border border-gray-200 shadow-xl">
                      {services.map(service => (
                        <SelectItem 
                          key={service.id} 
                          value={service.id.toString()} 
                          className="cursor-pointer hover:bg-gray-100 px-3 py-2"
                          onClick={() => console.log('Service cliqué:', service.nom_service)}
                        >
                          {service.nom_service}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="quotite_travail">Quotité de travail (h/semaine)</Label>
                  <Input
                    id="quotite_travail"
                    type="number"
                    value={agentForm.quotite_travail}
                    onChange={(e) => setAgentForm({...agentForm, quotite_travail: parseFloat(e.target.value) || 35})}
                    min="1"
                    max="40"
                  />
                </div>
                <div>
                  <Label htmlFor="date_debut_contrat">Date de début de contrat</Label>
                  <Input
                    id="date_debut_contrat"
                    type="date"
                    value={agentForm.date_debut_contrat}
                    onChange={(e) => setAgentForm({...agentForm, date_debut_contrat: e.target.value})}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="annee_entree_fp">Année d'entrée dans la FP</Label>
                  <Input
                    id="annee_entree_fp"
                    type="number"
                    value={agentForm.annee_entree_fp}
                    onChange={(e) => setAgentForm({...agentForm, annee_entree_fp: e.target.value})}
                    min="1900"
                    max="2030"
                  />
                </div>
                <div>
                  <Label htmlFor="date_fin_contrat">Date de fin de contrat (optionnel)</Label>
                  <Input
                    id="date_fin_contrat"
                    type="date"
                    value={agentForm.date_fin_contrat}
                    onChange={(e) => setAgentForm({...agentForm, date_fin_contrat: e.target.value})}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="solde_ca">Solde CA</Label>
                  <Input
                    id="solde_ca"
                    type="number"
                    value={agentForm.solde_ca}
                    onChange={(e) => setAgentForm({...agentForm, solde_ca: parseFloat(e.target.value) || 0})}
                    min="0"
                  />
                </div>
                <div>
                  <Label htmlFor="solde_rtt">Solde RTT</Label>
                  <Input
                    id="solde_rtt"
                    type="number"
                    value={agentForm.solde_rtt}
                    onChange={(e) => setAgentForm({...agentForm, solde_rtt: parseFloat(e.target.value) || 0})}
                    min="0"
                  />
                </div>
                <div>
                  <Label htmlFor="solde_cet">Solde CET</Label>
                  <Input
                    id="solde_cet"
                    type="number"
                    value={agentForm.solde_cet}
                    onChange={(e) => setAgentForm({...agentForm, solde_cet: parseFloat(e.target.value) || 0})}
                    min="0"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="solde_bonifications">Bonifications</Label>
                  <Input
                    id="solde_bonifications"
                    type="number"
                    value={agentForm.solde_bonifications}
                    onChange={(e) => setAgentForm({...agentForm, solde_bonifications: parseFloat(e.target.value) || 0})}
                    min="0"
                  />
                </div>
                <div>
                  <Label htmlFor="solde_jours_sujetions">Jours de sujétions</Label>
                  <Input
                    id="solde_jours_sujetions"
                    type="number"
                    value={agentForm.solde_jours_sujetions}
                    onChange={(e) => setAgentForm({...agentForm, solde_jours_sujetions: parseFloat(e.target.value) || 0})}
                    min="0"
                  />
                </div>
                <div>
                  <Label htmlFor="solde_conges_formations">Congés formations</Label>
                  <Input
                    id="solde_conges_formations"
                    type="number"
                    value={agentForm.solde_conges_formations}
                    onChange={(e) => setAgentForm({...agentForm, solde_conges_formations: parseFloat(e.target.value) || 0})}
                    min="0"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="solde_hs">Heures supplémentaires</Label>
                <Input
                  id="solde_hs"
                  type="number"
                  value={agentForm.solde_hs}
                  onChange={(e) => setAgentForm({...agentForm, solde_hs: parseFloat(e.target.value) || 0})}
                  min="0"
                />
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

export default AdminDashboardFixed

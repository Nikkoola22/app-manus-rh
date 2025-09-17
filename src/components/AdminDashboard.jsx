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
        fetch('/api/agents', { credentials: 'include' }),
        fetch('/api/services', { credentials: 'include' }),
        fetch('/api/demandes', { credentials: 'include' }),
        fetch('/api/arret-maladie', { credentials: 'include' })
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

  const handleAgentSubmit = async (e) => {
    e.preventDefault()
    try {
      const url = editingAgent ? `/api/agents/${editingAgent.id}` : '/api/agents'
      const method = editingAgent ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(agentForm),
      })

      if (response.ok) {
        await fetchData()
        setShowAgentForm(false)
        setEditingAgent(null)
        setAgentForm({
          nom: '',
          prenom: '',
          email: '',
          password: '',
          role: 'Agent',
          service_id: '',
          quotite_travail: 35,
          solde_ca: 0,
          solde_rtt: 0,
          solde_cet: 0
        })
      } else {
        const data = await response.json()
        alert(data.error || 'Erreur lors de la sauvegarde')
      }
    } catch (err) {
      alert('Erreur de connexion au serveur')
    }
  }

  const handleServiceSubmit = async (e) => {
    e.preventDefault()
    try {
      const url = editingService ? `/api/services/${editingService.id}` : '/api/services'
      const method = editingService ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(serviceForm),
      })

      if (response.ok) {
        await fetchData()
        setShowServiceForm(false)
        setEditingService(null)
        setServiceForm({
          nom_service: '',
          responsable_id: ''
        })
      } else {
        const data = await response.json()
        alert(data.error || 'Erreur lors de la sauvegarde')
      }
    } catch (err) {
      alert('Erreur de connexion au serveur')
    }
  }

  const startEditAgent = (agent) => {
    setEditingAgent(agent)
    setAgentForm({
      nom: agent.nom || '',
      prenom: agent.prenom || '',
      email: agent.email || '',
      password: '', // Ne pas pré-remplir le mot de passe
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
  }

  const startEditService = (service) => {
    setEditingService(service)
    setServiceForm({
      nom_service: service.nom_service || '',
      responsable_id: service.responsable_id ? service.responsable_id.toString() : ''
    })
    setShowServiceForm(true)
  }

  const startEditArretMaladie = (arret) => {
    setEditingArretMaladie(arret)
    setArretMaladieForm({
      agent_id: arret.agent_id ? arret.agent_id.toString() : '',
      date_debut: arret.date_debut || '',
      date_fin: arret.date_fin || '',
      motif: arret.motif || ''
    })
    setShowArretMaladieForm(true)
  }

  const handleDeleteAgent = async (agentId) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet agent ?')) {
      try {
        const response = await fetch(`/api/agents/${agentId}`, {
          method: 'DELETE',
          credentials: 'include',
        })

        if (response.ok) {
          await fetchData()
        } else {
          const data = await response.json()
          alert(data.error || 'Erreur lors de la suppression')
        }
      } catch (err) {
        alert('Erreur de connexion au serveur')
      }
    }
  }

  const handleDeleteService = async (serviceId) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce service ?')) {
      try {
        const response = await fetch(`/api/services/${serviceId}`, {
          method: 'DELETE',
          credentials: 'include',
        })

        if (response.ok) {
          await fetchData()
        } else {
          const data = await response.json()
          alert(data.error || 'Erreur lors de la suppression')
        }
      } catch (err) {
        alert('Erreur de connexion au serveur')
      }
    }

  const startEditAgent = (agent) => {
    setEditingAgent(agent)
    setAgentForm({
      nom: agent.nom,
      prenom: agent.prenom,
      email: agent.email,
      password: '',
      role: agent.role,
      service_id: agent.service_id || '',
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
  }

  const startEditService = (service) => {
    setEditingService(service)
    setServiceForm({
      nom_service: service.nom_service,
      responsable_id: service.responsable_id || ''
    })
    setShowServiceForm(true)
  }

  const handleArretMaladieSubmit = async (e) => {
    e.preventDefault()
    try {
      const url = editingArretMaladie ? `/api/arret-maladie/${editingArretMaladie.id}` : '/api/arret-maladie'
      const method = editingArretMaladie ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(arretMaladieForm),
      })

      if (response.ok) {
        await fetchData()
        setShowArretMaladieForm(false)
        setEditingArretMaladie(null)
        setArretMaladieForm({
          agent_id: '',
          date_debut: '',
          date_fin: '',
          motif: ''
        })
      } else {
        const data = await response.json()
        alert(data.error || 'Erreur lors de la sauvegarde')
      }
    } catch (err) {
      alert('Erreur de connexion au serveur')
    }
  }

  const handleDeleteArretMaladie = async (arretId) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet arrêt maladie ?')) {
      try {
        const response = await fetch(`/api/arret-maladie/${arretId}`, {
          method: 'DELETE',
          credentials: 'include',
        })

        if (response.ok) {
          await fetchData()
        } else {
          const data = await response.json()
          alert(data.error || 'Erreur lors de la suppression')
        }
      } catch (err) {
        alert('Erreur de connexion au serveur')
      }
    }
  }

  const startEditArretMaladie = (arret) => {
    setEditingArretMaladie(arret)
    setArretMaladieForm({
      agent_id: arret.agent_id.toString(),
      date_debut: arret.date_debut,
      date_fin: arret.date_fin,
      motif: arret.motif || ''
    })
    setShowArretMaladieForm(true)
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
                <Button onClick={() => {
                  setEditingAgent(null)
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
                  setShowAgentForm(true)
                }}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouvel agent
                </Button>
                
                <Dialog open={showAgentForm} onOpenChange={setShowAgentForm}>
                  <DialogContent className="max-w-2xl max-h-[90vh] bg-white border border-gray-200 shadow-xl overflow-hidden flex flex-col">
                    <DialogHeader className="flex-shrink-0">
                      <DialogTitle className="text-lg font-semibold text-gray-900">
                        {editingAgent ? 'Modifier l\'agent' : 'Nouvel agent'}
                      </DialogTitle>
                      <DialogDescription className="text-sm text-gray-600">
                        {editingAgent ? 'Modifiez les informations de l\'agent' : 'Créez un nouveau compte agent'}
                      </DialogDescription>
                    </DialogHeader>
                    <div className="flex-1 overflow-y-auto px-1">
                      <form id="agent-form" onSubmit={handleAgentSubmit} className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="nom">Nom *</Label>
                          <Input
                            id="nom"
                            value={agentForm.nom}
                            onChange={(e) => setAgentForm({...agentForm, nom: e.target.value})}
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="prenom">Prénom *</Label>
                          <Input
                            id="prenom"
                            value={agentForm.prenom}
                            onChange={(e) => setAgentForm({...agentForm, prenom: e.target.value})}
                            required
                          />
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="email">Email *</Label>
                        <Input
                          id="email"
                          type="email"
                          value={agentForm.email}
                          onChange={(e) => setAgentForm({...agentForm, email: e.target.value})}
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="password">
                          Mot de passe {editingAgent ? '(laisser vide pour ne pas changer)' : '*'}
                        </Label>
                        <Input
                          id="password"
                          type="password"
                          value={agentForm.password}
                          onChange={(e) => setAgentForm({...agentForm, password: e.target.value})}
                          required={!editingAgent}
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="role" className="text-sm font-medium text-gray-700">Rôle</Label>
                          <Select
                            value={agentForm.role}
                            onValueChange={(value) => setAgentForm({...agentForm, role: value})}
                          >
                            <SelectTrigger className="w-full bg-white border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent className="bg-white border border-gray-200 shadow-lg z-[100]">
                              <SelectItem value="Agent" className="hover:bg-gray-100 focus:bg-gray-100 cursor-pointer">Agent</SelectItem>
                              <SelectItem value="Responsable" className="hover:bg-gray-100 focus:bg-gray-100 cursor-pointer">Responsable</SelectItem>
                              <SelectItem value="Admin" className="hover:bg-gray-100 focus:bg-gray-100 cursor-pointer">Admin</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="service" className="text-sm font-medium text-gray-700">Service</Label>
                          <Select
                            value={agentForm.service_id}
                            onValueChange={(value) => setAgentForm({...agentForm, service_id: value})}
                          >
                            <SelectTrigger className="w-full bg-white border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                              <SelectValue placeholder="Sélectionner un service" />
                            </SelectTrigger>
                            <SelectContent className="bg-white border border-gray-200 shadow-lg z-[100] max-h-60 overflow-y-auto">
                              {services.length > 0 ? (
                                services.map((service) => (
                                  <SelectItem 
                                    key={service.id} 
                                    value={service.id.toString()}
                                    className="hover:bg-gray-100 focus:bg-gray-100 cursor-pointer"
                                  >
                                    {service.nom_service}
                                  </SelectItem>
                                ))
                              ) : (
                                <SelectItem value="" disabled className="text-gray-500">
                                  Aucun service disponible
                                </SelectItem>
                              )}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="quotite">Quotité de travail (h/semaine)</Label>
                          <Input
                            id="quotite"
                            type="number"
                            value={agentForm.quotite_travail}
                            onChange={(e) => setAgentForm({...agentForm, quotite_travail: parseFloat(e.target.value)})}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="date_debut_contrat">Date d'entrée</Label>
                          <Input
                            id="date_debut_contrat"
                            type="date"
                            value={agentForm.date_debut_contrat}
                            onChange={(e) => setAgentForm({...agentForm, date_debut_contrat: e.target.value})}
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="annee_entree_fp">Année d'entrée FP</Label>
                          <Input
                            id="annee_entree_fp"
                            type="number"
                            value={agentForm.annee_entree_fp}
                            onChange={(e) => setAgentForm({...agentForm, annee_entree_fp: parseInt(e.target.value)})}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="date_fin_contrat">Date de fin de contrat</Label>
                          <Input
                            id="date_fin_contrat"
                            type="date"
                            value={agentForm.date_fin_contrat}
                            onChange={(e) => setAgentForm({...agentForm, date_fin_contrat: e.target.value})}
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="solde_ca">Solde CA (heures)</Label>
                          <Input
                            id="solde_ca"
                            type="number"
                            step="0.5"
                            value={agentForm.solde_ca}
                            onChange={(e) => setAgentForm({...agentForm, solde_ca: parseFloat(e.target.value)})}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="solde_hs">Solde HS (heures)</Label>
                          <Input
                            id="solde_hs"
                            type="number"
                            step="0.5"
                            value={agentForm.solde_hs}
                            onChange={(e) => setAgentForm({...agentForm, solde_hs: parseFloat(e.target.value)})}
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="solde_rtt">Solde RTT (heures)</Label>
                          <Input
                            id="solde_rtt"
                            type="number"
                            step="0.5"
                            value={agentForm.solde_rtt}
                            onChange={(e) => setAgentForm({...agentForm, solde_rtt: parseFloat(e.target.value)})}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="solde_cet">Solde CET (heures)</Label>
                          <Input
                            id="solde_cet"
                            type="number"
                            step="0.5"
                            value={agentForm.solde_cet}
                            onChange={(e) => setAgentForm({...agentForm, solde_cet: parseFloat(e.target.value)})}
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="solde_bonifications">Solde Bonifications (heures)</Label>
                          <Input
                            id="solde_bonifications"
                            type="number"
                            step="0.5"
                            value={agentForm.solde_bonifications}
                            onChange={(e) => setAgentForm({...agentForm, solde_bonifications: parseFloat(e.target.value)})}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="solde_jours_sujetions">Solde Jours de sujétions (heures)</Label>
                          <Input
                            id="solde_jours_sujetions"
                            type="number"
                            step="0.5"
                            value={agentForm.solde_jours_sujetions}
                            onChange={(e) => setAgentForm({...agentForm, solde_jours_sujetions: parseFloat(e.target.value)})}
                          />
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="solde_conges_formations">Solde Congés formations (heures)</Label>
                        <Input
                          id="solde_conges_formations"
                          type="number"
                          step="0.5"
                          value={agentForm.solde_conges_formations}
                          onChange={(e) => setAgentForm({...agentForm, solde_conges_formations: parseFloat(e.target.value)})}
                        />
                      </div>
                      </form>
                    </div>
                    <div className="flex-shrink-0 flex justify-end space-x-2 pt-4 border-t border-gray-200">
                      <Button type="button" variant="outline" onClick={() => setShowAgentForm(false)}>
                        Annuler
                      </Button>
                      <Button type="submit" form="agent-form">
                        {editingAgent ? 'Modifier' : 'Créer'}
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
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
                              onClick={() => startEditAgent(agent)}
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
                <Button onClick={() => {
                  setEditingService(null)
                  setServiceForm({
                    nom_service: '',
                    responsable_id: ''
                  })
                  setShowServiceForm(true)
                }}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouveau service
                </Button>
                
                <Dialog open={showServiceForm} onOpenChange={setShowServiceForm}>
                  <DialogContent className="sm:max-w-[425px] bg-white border border-gray-200 shadow-xl">
                    <DialogHeader>
                      <DialogTitle className="text-lg font-semibold text-gray-900">
                        {editingService ? 'Modifier le service' : 'Nouveau service'}
                      </DialogTitle>
                      <DialogDescription className="text-sm text-gray-600">
                        {editingService ? 'Modifiez les informations du service' : 'Créez un nouveau service'}
                      </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleServiceSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="nom_service" className="text-sm font-medium text-gray-700">Nom du service *</Label>
                        <Input
                          id="nom_service"
                          value={serviceForm.nom_service}
                          onChange={(e) => setServiceForm({...serviceForm, nom_service: e.target.value})}
                          className="w-full"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="responsable" className="text-sm font-medium text-gray-700">Responsable</Label>
                        <Select
                          value={serviceForm.responsable_id}
                          onValueChange={(value) => setServiceForm({...serviceForm, responsable_id: value})}
                        >
                          <SelectTrigger className="w-full bg-white border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                            <SelectValue placeholder="Sélectionner un responsable" />
                          </SelectTrigger>
                          <SelectContent className="bg-white border border-gray-200 shadow-lg z-[100] max-h-60 overflow-y-auto">
                            {agents.filter(a => a.role === 'Responsable' || a.role === 'Admin').length > 0 ? (
                              agents.filter(a => a.role === 'Responsable' || a.role === 'Admin').map((agent) => (
                                <SelectItem 
                                  key={agent.id} 
                                  value={agent.id.toString()}
                                  className="hover:bg-gray-100 focus:bg-gray-100 cursor-pointer"
                                >
                                  {agent.prenom} {agent.nom}
                                </SelectItem>
                              ))
                            ) : (
                              <SelectItem value="" disabled className="text-gray-500">
                                Aucun responsable disponible
                              </SelectItem>
                            )}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="flex justify-end space-x-2 pt-4">
                        <Button 
                          type="button" 
                          variant="outline" 
                          onClick={() => setShowServiceForm(false)}
                          className="px-4 py-2"
                        >
                          Annuler
                        </Button>
                        <Button 
                          type="submit"
                          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white"
                        >
                          {editingService ? 'Modifier' : 'Créer'}
                        </Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
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
                              onClick={() => startEditService(service)}
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
                <Button onClick={() => {
                  setEditingArretMaladie(null)
                  setArretMaladieForm({
                    agent_id: '',
                    date_debut: '',
                    date_fin: '',
                    motif: ''
                  })
                  setShowArretMaladieForm(true)
                }}>
                  <Stethoscope className="h-4 w-4 mr-2" />
                  Nouvel arrêt maladie
                </Button>
                
                <Dialog open={showArretMaladieForm} onOpenChange={setShowArretMaladieForm}>
                  <DialogContent className="sm:max-w-[425px] bg-white border border-gray-200 shadow-xl">
                    <DialogHeader>
                      <DialogTitle className="text-lg font-semibold text-gray-900">
                        {editingArretMaladie ? 'Modifier l\'arrêt maladie' : 'Nouvel arrêt maladie'}
                      </DialogTitle>
                      <DialogDescription className="text-sm text-gray-600">
                        {editingArretMaladie ? 'Modifiez les informations de l\'arrêt maladie' : 'Enregistrez un nouvel arrêt maladie'}
                      </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleArretMaladieSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="agent_arret" className="text-sm font-medium text-gray-700">Agent *</Label>
                        <Select
                          value={arretMaladieForm.agent_id}
                          onValueChange={(value) => setArretMaladieForm({...arretMaladieForm, agent_id: value})}
                        >
                          <SelectTrigger className="w-full bg-white border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                            <SelectValue placeholder="Sélectionner un agent" />
                          </SelectTrigger>
                          <SelectContent className="bg-white border border-gray-200 shadow-lg z-[100] max-h-60 overflow-y-auto">
                            {agents.length > 0 ? (
                              agents.map((agent) => (
                                <SelectItem 
                                  key={agent.id} 
                                  value={agent.id.toString()}
                                  className="hover:bg-gray-100 focus:bg-gray-100 cursor-pointer"
                                >
                                  {agent.prenom} {agent.nom} - {agent.quotite_travail}h/semaine
                                </SelectItem>
                              ))
                            ) : (
                              <SelectItem value="" disabled className="text-gray-500">
                                Aucun agent disponible
                              </SelectItem>
                            )}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="date_debut_arret">Date de début *</Label>
                          <Input
                            id="date_debut_arret"
                            type="date"
                            value={arretMaladieForm.date_debut}
                            onChange={(e) => setArretMaladieForm({...arretMaladieForm, date_debut: e.target.value})}
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="date_fin_arret">Date de fin *</Label>
                          <Input
                            id="date_fin_arret"
                            type="date"
                            value={arretMaladieForm.date_fin}
                            onChange={(e) => setArretMaladieForm({...arretMaladieForm, date_fin: e.target.value})}
                            required
                          />
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="motif_arret">Motif</Label>
                        <Textarea
                          id="motif_arret"
                          placeholder="Décrivez le motif de l'arrêt maladie..."
                          value={arretMaladieForm.motif}
                          onChange={(e) => setArretMaladieForm({...arretMaladieForm, motif: e.target.value})}
                          rows={3}
                        />
                      </div>
                      {arretMaladieForm.agent_id && arretMaladieForm.date_debut && arretMaladieForm.date_fin && (
                        <div className="bg-blue-50 p-3 rounded-md">
                          <p className="text-sm text-blue-800">
                            <strong>Information :</strong> Si l'agent est à 38h/semaine ou plus, 
                            il perdra 1 jour de RTT tous les 13 jours d'arrêt maladie.
                          </p>
                        </div>
                      )}
                      <div className="flex justify-end space-x-2">
                        <Button type="button" variant="outline" onClick={() => setShowArretMaladieForm(false)}>
                          Annuler
                        </Button>
                        <Button type="submit">
                          {editingArretMaladie ? 'Modifier' : 'Enregistrer'}
                        </Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
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
                              onClick={() => startEditArretMaladie(arret)}
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
}
export default AdminDashboard


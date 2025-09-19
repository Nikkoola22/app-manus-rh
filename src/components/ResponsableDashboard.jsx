import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import api from '../services/api'
import { 
  Users, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Eye, 
  Stethoscope, 
  Edit, 
  Trash2, 
  Calendar as CalendarIcon, 
  Plus,
  CalendarDays
} from 'lucide-react'
import Calendar from './Calendar'
import PlanningAgent from './PlanningAgent'
import PlanningEditorTime from './PlanningEditorTime'

const ResponsableDashboard = ({ user, onViewAgent }) => {
  const [demandes, setDemandes] = useState([])
  const [agents, setAgents] = useState([])
  const [arretsMaladie, setArretsMaladie] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedDemande, setSelectedDemande] = useState(null)
  const [commentaires, setCommentaires] = useState('')
  const [actionLoading, setActionLoading] = useState(false)
  const [showArretMaladieForm, setShowArretMaladieForm] = useState(false)
  const [editingArretMaladie, setEditingArretMaladie] = useState(null)
  const [showDemandeForm, setShowDemandeForm] = useState(false)
  const [mesDemandes, setMesDemandes] = useState([])
  const [selectedAgentPlanning, setSelectedAgentPlanning] = useState(null)
  const [showPlanningEditor, setShowPlanningEditor] = useState(false)
  const [planningRefreshTrigger, setPlanningRefreshTrigger] = useState(0)
  const [activeTab, setActiveTab] = useState('demandes-attente')

  // Refs pour le scroll automatique
  const demandesAttenteRef = useRef(null)
  const demandesTraiteesRef = useRef(null)
  const mesDemandesRef = useRef(null)

  const [arretMaladieForm, setArretMaladieForm] = useState({
    agent_id: '',
    date_debut: '',
    date_fin: '',
    motif: ''
  })

  const [demandeForm, setDemandeForm] = useState({
    type_absence: 'CA',
    date_debut: '',
    date_fin: '',
    nb_heures: 7,
    motif: ''
  })

  useEffect(() => {
    fetchData()
  }, [])

  // Effect pour gérer le scroll automatique quand l'onglet change
  useEffect(() => {
    console.log('Active tab changed to:', activeTab) // Debug log
    
    // Attendre un délai pour que le contenu soit rendu
    const timer = setTimeout(() => {
      console.log('Attempting scroll for active tab:', activeTab) // Debug log
      
      // Essayer d'abord avec les refs
      let element = null
      
      if (activeTab === 'demandes-attente') {
        element = demandesAttenteRef.current || document.getElementById('demandes-attente-section')
        console.log('Demandes attente element:', element) // Debug log
      } else if (activeTab === 'demandes-traitees') {
        element = demandesTraiteesRef.current || document.getElementById('demandes-traitees-section')
        console.log('Demandes traitees element:', element) // Debug log
      } else if (activeTab === 'mes-demandes') {
        element = mesDemandesRef.current || document.getElementById('mes-demandes-section')
        console.log('Mes demandes element:', element) // Debug log
      }
      
      if (element) {
        console.log('Scrolling to element:', element) // Debug log
        element.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start',
          inline: 'nearest'
        })
      } else {
        console.log('No element found for tab:', activeTab) // Debug log
      }
    }, 300) // Délai plus long pour s'assurer que le contenu est rendu

    return () => clearTimeout(timer)
  }, [activeTab])

  const fetchData = async () => {
    try {
      const [demandesResponse, agentsResponse, arretsMaladieResponse, mesDemandesResponse] = await Promise.all([
        api.getDemandes(),
        api.getAgents(),
        api.getArretsMaladie(),
        api.getMesDemandes()
      ])

      if (demandesResponse.ok) {
        const demandesData = await demandesResponse.json()
        setDemandes(demandesData)
      }

      if (agentsResponse.ok) {
        const agentsData = await agentsResponse.json()
        setAgents(agentsData)
      }

      if (arretsMaladieResponse.ok) {
        const arretsMaladieData = await arretsMaladieResponse.json()
        setArretsMaladie(arretsMaladieData)
      }

      if (mesDemandesResponse.ok) {
        const mesDemandesData = await mesDemandesResponse.json()
        setMesDemandes(mesDemandesData)
      }
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleValidation = async (demandeId, action) => {
    setActionLoading(true)
    try {
      let response
      if (action === 'approuver') {
        response = await api.validerDemande(demandeId)
      } else if (action === 'refuser') {
        response = await api.rejeterDemande(demandeId)
      }

      if (response && response.success) {
        await fetchData() // Recharger les données
        setSelectedDemande(null)
        setCommentaires('')
        alert(response.message || 'Action effectuée avec succès')
      } else {
        alert(response?.error || 'Erreur lors de l\'action')
      }
    } catch (err) {
      console.error('Erreur lors de la validation:', err)
      alert('Erreur de connexion au serveur')
    } finally {
      setActionLoading(false)
    }
  }

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

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR')
  }

  const formatHours = (hours) => {
    return `${hours}h`
  }

  const demandesEnAttente = demandes.filter(d => d.statut === 'En attente')
  const demandesTraitees = demandes.filter(d => d.statut !== 'En attente')

  const totalSoldeCA = agents.reduce((sum, agent) => sum + (agent.solde_ca || 0), 0)
  const totalSoldeRTT = agents.reduce((sum, agent) => sum + (agent.solde_rtt || 0), 0)

  // Fonction pour créer une demande de congé
  const handleDemandeSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await api.createDemande({
        agent_id: user.id,
        ...demandeForm
      })

      if (response.ok) {
        await fetchData()
        setShowDemandeForm(false)
        setDemandeForm({
          type_absence: 'CA',
          date_debut: '',
          date_fin: '',
          nb_heures: 7,
          motif: ''
        })
        alert('Demande de congé créée avec succès')
      } else {
        const errorData = await response.json()
        alert(`Erreur: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Erreur lors de la création de la demande:', error)
      alert('Erreur lors de la création de la demande')
    }
  }

  // Fonctions pour gérer les arrêts maladie
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
        const response = await api.deleteArretMaladie(arretId)

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

  const handleEditPlanning = (agent) => {
    setSelectedAgentPlanning(agent)
    setShowPlanningEditor(true)
  }

  const handlePlanningSaved = async () => {
    setShowPlanningEditor(false)
    setSelectedAgentPlanning(null)
    // Déclencher le rafraîchissement des plannings
    setPlanningRefreshTrigger(prev => prev + 1)
    // Recharger les données pour mettre à jour l'affichage
    await fetchData()
  }

  const handlePlanningCancel = () => {
    setShowPlanningEditor(false)
    setSelectedAgentPlanning(null)
  }

  // Fonction pour gérer le changement d'onglet
  const handleTabChange = (value) => {
    console.log('Tab changed to:', value) // Debug log
    setActiveTab(value) // Mettre à jour l'état pour déclencher l'useEffect
  }

  return (
    <div className="space-y-6">
      {/* Statistiques du service */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Agents du service</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{agents.length}</div>
            <p className="text-xs text-muted-foreground">Total agents</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Demandes en attente</CardTitle>
            <AlertCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{demandesEnAttente.length}</div>
            <p className="text-xs text-muted-foreground">À traiter</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total CA Service</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatHours(totalSoldeCA)}</div>
            <p className="text-xs text-muted-foreground">Congés annuels</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total RTT Service</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatHours(totalSoldeRTT)}</div>
            <p className="text-xs text-muted-foreground">RTT disponibles</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="demandes-attente" className="space-y-4" onValueChange={handleTabChange}>
        <TabsList>
          <TabsTrigger value="demandes-attente">
            Demandes en attente ({demandesEnAttente.length})
          </TabsTrigger>
          <TabsTrigger value="demandes-traitees">
            Demandes traitées ({demandesTraitees.length})
          </TabsTrigger>
          <TabsTrigger value="mes-demandes">
            Mes Demandes ({mesDemandes.length})
          </TabsTrigger>
          <TabsTrigger value="agents">
            Agents du service ({agents.length})
          </TabsTrigger>
          <TabsTrigger value="arrets-maladie">
            Arrêts maladie ({arretsMaladie.length})
          </TabsTrigger>
          <TabsTrigger value="calendrier">
            <CalendarIcon className="h-4 w-4 mr-2" />
            Calendrier
          </TabsTrigger>
          <TabsTrigger value="planning">
            <CalendarDays className="h-4 w-4 mr-2" />
            Planning
          </TabsTrigger>
        </TabsList>

        <TabsContent value="demandes-attente">
          <div ref={demandesAttenteRef} id="demandes-attente-section">
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
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>Date demande</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {demandesEnAttente.map((demande) => (
                      <TableRow key={demande.id}>
                        <TableCell className="font-medium">
                          {demande.agent?.prenom} {demande.agent?.nom}
                        </TableCell>
                        <TableCell>{demande.type_absence}</TableCell>
                        <TableCell>
                          {formatDate(demande.date_debut)} - {formatDate(demande.date_fin)}
                        </TableCell>
                        <TableCell>{formatHours(demande.nb_heures)}</TableCell>
                        <TableCell>{formatDate(demande.date_demande)}</TableCell>
                        <TableCell>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setSelectedDemande(demande)}
                          >
                            Traiter
                          </Button>
                          
                          <Dialog open={!!selectedDemande}>
                            <DialogContent onClose={() => setSelectedDemande(null)}>
                              <DialogHeader onClose={() => setSelectedDemande(null)}>
                                <DialogTitle>Validation de la demande</DialogTitle>
                                <DialogDescription>
                                  Demande de {demande.agent?.prenom} {demande.agent?.nom}
                                </DialogDescription>
                              </DialogHeader>
                              <div className="space-y-4">
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                  <div>
                                    <strong>Type:</strong> {demande.type_absence}
                                  </div>
                                  <div>
                                    <strong>Durée:</strong> {formatHours(demande.nb_heures)}
                                  </div>
                                  <div>
                                    <strong>Du:</strong> {formatDate(demande.date_debut)}
                                  </div>
                                  <div>
                                    <strong>Au:</strong> {formatDate(demande.date_fin)}
                                  </div>
                                </div>
                                {demande.motif && (
                                  <div>
                                    <strong>Motif:</strong> {demande.motif}
                                  </div>
                                )}
                                <div className="space-y-2">
                                  <Label htmlFor="commentaires">Commentaires (optionnel)</Label>
                                  <Textarea
                                    id="commentaires"
                                    placeholder="Ajoutez un commentaire..."
                                    value={commentaires}
                                    onChange={(e) => setCommentaires(e.target.value)}
                                  />
                                </div>
                                <div className="flex justify-end space-x-2">
                                  <Button
                                    variant="outline"
                                    onClick={() => handleValidation(demande.id, 'refuser')}
                                    disabled={actionLoading}
                                  >
                                    <XCircle className="h-4 w-4 mr-2" />
                                    Refuser
                                  </Button>
                                  <Button
                                    onClick={() => handleValidation(demande.id, 'approuver')}
                                    disabled={actionLoading}
                                  >
                                    <CheckCircle className="h-4 w-4 mr-2" />
                                    Approuver
                                  </Button>
                                </div>
                              </div>
                            </DialogContent>
                          </Dialog>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
          </div>
        </TabsContent>

        <TabsContent value="demandes-traitees">
          <div ref={demandesTraiteesRef} id="demandes-traitees-section">
          <Card>
            <CardHeader>
              <CardTitle>Demandes traitées</CardTitle>
              <CardDescription>
                Historique des demandes validées ou refusées
              </CardDescription>
            </CardHeader>
            <CardContent>
              {demandesTraitees.length === 0 ? (
                <div className="text-center py-4 text-muted-foreground">
                  Aucune demande traitée
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>Statut</TableHead>
                      <TableHead>Validé le</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {demandesTraitees.map((demande) => (
                      <TableRow key={demande.id}>
                        <TableCell className="font-medium">
                          {demande.agent?.prenom} {demande.agent?.nom}
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
                        <TableCell>
                          {demande.date_validation ? formatDate(demande.date_validation) : '-'}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
          </div>
        </TabsContent>

        <TabsContent value="mes-demandes">
          <div ref={mesDemandesRef} id="mes-demandes-section">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Mes Demandes de Congés</CardTitle>
                  <CardDescription>
                    Créer et suivre vos demandes de congés (validées par l'admin)
                  </CardDescription>
                </div>
                <Button onClick={() => setShowDemandeForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nouvelle Demande
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {mesDemandes.length === 0 ? (
                <div className="text-center py-8">
                  <CalendarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Aucune demande de congé</p>
                  <Button 
                    onClick={() => setShowDemandeForm(true)}
                    className="mt-4"
                  >
                    Créer ma première demande
                  </Button>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Type</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>Motif</TableHead>
                      <TableHead>Statut</TableHead>
                      <TableHead>Date de demande</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {mesDemandes.map((demande) => (
                      <TableRow key={demande.id}>
                        <TableCell className="font-medium">
                          {demande.type_absence}
                        </TableCell>
                        <TableCell>
                          {formatDate(demande.date_debut)} - {formatDate(demande.date_fin)}
                        </TableCell>
                        <TableCell>{formatHours(demande.nb_heures)}</TableCell>
                        <TableCell>{demande.motif}</TableCell>
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
          </div>
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
              {agents.length === 0 ? (
                <div className="text-center py-4 text-muted-foreground">
                  Aucun agent dans ce service
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>CA</TableHead>
                      <TableHead>RTT</TableHead>
                      <TableHead>CET</TableHead>
                        <TableHead>Quotité</TableHead>
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
                          <TableCell>{formatHours(agent.solde_ca || 0)}</TableCell>
                          <TableCell>{formatHours(agent.solde_rtt || 0)}</TableCell>
                          <TableCell>{formatHours(agent.solde_cet || 0)}</TableCell>
                          <TableCell>{agent.quotite_travail || '-'}h</TableCell>
                          <TableCell>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => onViewAgent && onViewAgent(agent.id)}
                              title="Voir le profil"
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                          </TableCell>
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
                  <CardTitle>Arrêts maladie du service</CardTitle>
                  <CardDescription>
                    Enregistrer et gérer les arrêts maladie des agents de votre service
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
                
                <Dialog open={showArretMaladieForm}>
                  <DialogContent onClose={() => setShowArretMaladieForm(false)}>
                    <DialogHeader onClose={() => setShowArretMaladieForm(false)}>
                      <DialogTitle>
                        {editingArretMaladie ? 'Modifier l\'arrêt maladie' : 'Nouvel arrêt maladie'}
                      </DialogTitle>
                      <DialogDescription>
                        {editingArretMaladie ? 'Modifiez les informations de l\'arrêt maladie' : 'Enregistrez un nouvel arrêt maladie'}
                      </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleArretMaladieSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="agent_arret">Agent *</Label>
                        <Select
                          value={arretMaladieForm.agent_id}
                          onValueChange={(value) => setArretMaladieForm({...arretMaladieForm, agent_id: value})}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Sélectionner un agent" />
                          </SelectTrigger>
                          <SelectContent>
                            {agents.map((agent) => (
                              <SelectItem key={agent.id} value={agent.id.toString()}>
                                {agent.prenom} {agent.nom} - {agent.quotite_travail}h/semaine
                              </SelectItem>
                            ))}
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

        <TabsContent value="calendrier">
          <Calendar user={user} />
        </TabsContent>

        <TabsContent value="planning">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <CalendarDays className="h-5 w-5 mr-2" />
                Planning des agents
              </CardTitle>
              <CardDescription>
                Gestion des horaires de travail des agents du service
              </CardDescription>
            </CardHeader>
            <CardContent>
              {agents.length === 0 ? (
                <div className="text-center py-8">
                  <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Aucun agent dans ce service</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {agents.map((agent) => (
                    <div key={agent.id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h3 className="font-semibold text-lg">
                            {agent.prenom} {agent.nom}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {agent.email}
                          </p>
                        </div>
                        <Button
                          onClick={() => handleEditPlanning(agent)}
                          variant="outline"
                          size="sm"
                        >
                          <Edit className="h-4 w-4 mr-2" />
                          Modifier le planning
                        </Button>
                      </div>
                      <PlanningAgent
                        agentId={agent.id}
                        agentName={`${agent.prenom} ${agent.nom}`}
                        canEdit={true}
                        refreshTrigger={planningRefreshTrigger}
                      />
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Formulaire de création de demande de congé */}
      <Dialog open={showDemandeForm} onOpenChange={setShowDemandeForm}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Nouvelle Demande de Congé</DialogTitle>
            <DialogDescription>
              Créer une nouvelle demande de congé (sera validée par l'admin)
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleDemandeSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="type_absence">Type d'absence</Label>
              <Select
                value={demandeForm.type_absence}
                onValueChange={(value) => setDemandeForm({ ...demandeForm, type_absence: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner un type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="CA">Congés Annuels (CA)</SelectItem>
                  <SelectItem value="RTT">RTT</SelectItem>
                  <SelectItem value="CET">Compte Épargne Temps (CET)</SelectItem>
                  <SelectItem value="HS">Heures Supplémentaires (HS)</SelectItem>
                  <SelectItem value="Bonifications">Bonifications</SelectItem>
                  <SelectItem value="Jours de sujétions">Jours de sujétions</SelectItem>
                  <SelectItem value="Congés formations">Congés formations</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="date_debut">Date de début</Label>
                <Input
                  id="date_debut"
                  type="date"
                  value={demandeForm.date_debut}
                  onChange={(e) => setDemandeForm({ ...demandeForm, date_debut: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="date_fin">Date de fin</Label>
                <Input
                  id="date_fin"
                  type="date"
                  value={demandeForm.date_fin}
                  onChange={(e) => setDemandeForm({ ...demandeForm, date_fin: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="nb_heures">Nombre d'heures</Label>
              <Input
                id="nb_heures"
                type="number"
                step="0.5"
                min="0.5"
                max="35"
                value={demandeForm.nb_heures}
                onChange={(e) => setDemandeForm({ ...demandeForm, nb_heures: parseFloat(e.target.value) })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="motif">Motif</Label>
              <Textarea
                id="motif"
                placeholder="Décrivez le motif de votre demande..."
                value={demandeForm.motif}
                onChange={(e) => setDemandeForm({ ...demandeForm, motif: e.target.value })}
                required
              />
            </div>

            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={() => setShowDemandeForm(false)}>
                Annuler
              </Button>
              <Button type="submit">
                Créer la demande
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      {/* Dialog pour éditer le planning */}
      {showPlanningEditor && selectedAgentPlanning && (
        <Dialog open={showPlanningEditor} onOpenChange={setShowPlanningEditor}>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <PlanningEditorTime
              agentId={selectedAgentPlanning.id}
              agentName={`${selectedAgentPlanning.prenom} ${selectedAgentPlanning.nom}`}
              onSave={handlePlanningSaved}
              onCancel={handlePlanningCancel}
            />
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}

export default ResponsableDashboard


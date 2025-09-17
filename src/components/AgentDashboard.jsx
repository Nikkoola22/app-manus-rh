import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Plus, Clock, Calendar, FileText, AlertCircle, User, Briefcase, CalendarDays, X } from 'lucide-react'
import DemandeForm from './DemandeForm'
import PlanningAgent from './PlanningAgent'

const AgentDashboard = ({ user }) => {
  const [demandes, setDemandes] = useState([])
  const [arretsMaladie, setArretsMaladie] = useState([])
  const [loading, setLoading] = useState(true)
  const [showDemandeForm, setShowDemandeForm] = useState(false)
  const [planningRefreshTrigger, setPlanningRefreshTrigger] = useState(0)

  useEffect(() => {
    fetchDemandes()
    fetchArretsMaladie()
  }, [])

  const fetchDemandes = async () => {
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

  const fetchArretsMaladie = async () => {
    try {
      const response = await fetch(`/api/arret-maladie?agent_id=${user.id}`, {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setArretsMaladie(data)
      }
    } catch (err) {
      console.error('Erreur lors du chargement des arrêts maladie:', err)
    }
  }

  const annulerDemande = async (demandeId) => {
    if (!confirm('Êtes-vous sûr de vouloir annuler cette demande ?')) {
      return
    }

    try {
      const response = await fetch(`/api/demandes/${demandeId}/annuler`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const result = await response.json()
        alert('Demande annulée avec succès')
        // Recharger les demandes
        await fetchDemandes()
      } else {
        const error = await response.json()
        alert('Erreur lors de l\'annulation: ' + error.error)
      }
    } catch (err) {
      console.error('Erreur lors de l\'annulation:', err)
      alert('Erreur de connexion lors de l\'annulation')
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

  const formatDays = (days) => {
    if (!days) return '0 jour'
    if (days === 1) return '1 jour'
    if (days === 0.5) return '0.5 jour'
    return `${Math.round(days * 10) / 10} jours`
  }

  const formatSolde = (type, value) => {
    if (!value) return type === 'CA' ? '0 jour' : '0h'
    
    if (type === 'CA') {
      if (value === 1) return '1 jour'
      if (value === 0.5) return '0.5 jour'
      return `${Math.round(value * 10) / 10} jours`
    } else {
      return `${Math.round(value * 10) / 10}h`
    }
  }

  const handleDemandeCreated = () => {
    setShowDemandeForm(false)
    fetchDemandes()
  }

  // Fonction pour calculer le total des congés pris par type
  const calculateCongesPris = (typeAbsence) => {
    if (!demandes || !user) return 0
    
    return demandes
      .filter(demande => demande.type_absence === typeAbsence && demande.statut === 'Approuvée')
      .reduce((total, demande) => total + (demande.nb_heures || 0), 0)
  }

  // Fonction pour calculer le solde avant une demande
  const calculateSoldeAvant = (typeAbsence, index) => {
    if (!user) return 0
    
    const soldeInitial = getSoldeInitial(typeAbsence)
    const demandesAvant = demandes
      .filter(demande => demande.type_absence === typeAbsence && demande.statut === 'Approuvée')
      .sort((a, b) => new Date(a.date_demande) - new Date(b.date_demande))
      .slice(0, index)
    
    const totalPris = demandesAvant.reduce((total, demande) => total + (demande.nb_heures || 0), 0)
    return soldeInitial - totalPris
  }

  // Fonction pour calculer le solde après une demande
  const calculateSoldeApres = (typeAbsence, index) => {
    if (!user) return 0
    
    const soldeInitial = getSoldeInitial(typeAbsence)
    const demandesAvant = demandes
      .filter(demande => demande.type_absence === typeAbsence && demande.statut === 'Approuvée')
      .sort((a, b) => new Date(a.date_demande) - new Date(b.date_demande))
      .slice(0, index + 1)
    
    const totalPris = demandesAvant.reduce((total, demande) => total + (demande.nb_heures || 0), 0)
    return soldeInitial - totalPris
  }

  // Fonction pour calculer les RTT selon la quotité de travail (en heures)
  const calculateRttFromQuotite = (quotite) => {
    if (!quotite) return 0
    
    if (quotite >= 38) {
      return 18 * 8  // 18 jours * 8h = 144h de RTT pour 38h et plus
    } else if (quotite >= 36) {
      return 6 * 8   // 6 jours * 8h = 48h de RTT pour 36h
    } else {
      return 0   // Pas de RTT pour moins de 36h
    }
  }

  // Fonction pour obtenir le solde initial selon le type
  const getSoldeInitial = (typeAbsence) => {
    if (!user) return 0
    
    switch (typeAbsence) {
      case 'CA':
        return user.solde_ca || 0
      case 'RTT':
        return calculateRttFromQuotite(user.quotite_travail)  // Calcul automatique des RTT
      case 'CET':
        return user.solde_cet || 0
      case 'Bonifications':
        return user.solde_bonifications || 0
      case 'Jours de sujétions':
        return user.solde_jours_sujetions || 0
      case 'Congés formations':
        return user.solde_conges_formations || 0
      case 'HS':
        return user.solde_hs || 0
      default:
        return 0
    }
  }


  if (showDemandeForm) {
    return (
      <DemandeForm
        user={user}
        onCancel={() => setShowDemandeForm(false)}
        onSuccess={handleDemandeCreated}
      />
    )
  }

  return (
    <div className="space-y-6">
      <Tabs defaultValue="dashboard" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="dashboard" className="flex items-center">
            <User className="h-4 w-4 mr-2" />
            Tableau de bord
          </TabsTrigger>
          <TabsTrigger value="planning" className="flex items-center">
            <CalendarDays className="h-4 w-4 mr-2" />
            Mon planning
          </TabsTrigger>
          <TabsTrigger value="historique" className="flex items-center">
            <FileText className="h-4 w-4 mr-2" />
            Historique
          </TabsTrigger>
        </TabsList>

        <TabsContent value="dashboard" className="space-y-6">
      {/* Informations personnelles */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <User className="h-5 w-5 mr-2" />
              Mes informations
            </CardTitle>
            <CardDescription>
              Vos informations personnelles et professionnelles
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <label className="text-sm font-medium text-gray-500">Nom complet</label>
                <p className="text-sm font-medium">{user.prenom} {user.nom}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Email</label>
                <p className="text-sm">{user.email}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Service</label>
                <p className="text-sm">{user.service?.nom_service || 'Non assigné'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Rôle</label>
                <p className="text-sm">{user.role}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Briefcase className="h-5 w-5 mr-2" />
              Informations de travail
            </CardTitle>
            <CardDescription>
              Vos conditions de travail et dates importantes
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <label className="text-sm font-medium text-gray-500">Date d'arrivée</label>
                <p className="text-sm font-medium">{formatDate(user.date_debut_contrat)}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Quotité de travail</label>
                <p className="text-sm font-medium">{user.quotite_travail}h/semaine</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Année d'entrée FP</label>
                <p className="text-sm">{user.annee_entree_fp || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Fin de contrat</label>
                <p className="text-sm">{user.date_fin_contrat ? formatDate(user.date_fin_contrat) : 'CDI'}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Soldes de congés */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Congés Annuels</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatSolde('CA', user.solde_ca || 0)}</div>
            <p className="text-xs text-muted-foreground">Solde disponible</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">RTT</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatSolde('RTT', user.solde_rtt || 0)}</div>
            <p className="text-xs text-muted-foreground">Solde disponible</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">CET</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatSolde('CET', user.solde_cet || 0)}</div>
            <p className="text-xs text-muted-foreground">Compte Épargne Temps</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Heures Supplémentaires</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatSolde('HS', user.solde_hs || 0)}</div>
            <p className="text-xs text-muted-foreground">Solde disponible</p>
          </CardContent>
        </Card>
      </div>

      {/* Actions rapides */}
      <Card>
        <CardHeader>
          <CardTitle>Actions rapides</CardTitle>
          <CardDescription>
            Gérez vos demandes de congés et RTT
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={() => setShowDemandeForm(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Nouvelle demande
          </Button>
        </CardContent>
      </Card>

      {/* Mes demandes */}
      <Card>
        <CardHeader>
          <CardTitle>Mes demandes</CardTitle>
          <CardDescription>
            Historique et statut de vos demandes de congés
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-4">Chargement...</div>
          ) : demandes.length === 0 ? (
            <div className="text-center py-4 text-muted-foreground">
              Aucune demande trouvée
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Type</TableHead>
                  <TableHead>Période</TableHead>
                  <TableHead>Durée</TableHead>
                  <TableHead>Statut</TableHead>
                  <TableHead>Date demande</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {demandes.map((demande) => (
                  <TableRow key={demande.id}>
                    <TableCell className="font-medium">
                      {demande.type_absence}
                    </TableCell>
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
                    <TableCell>
                      {demande.statut === 'En attente' && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => annulerDemande(demande.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <X className="h-4 w-4 mr-1" />
                          Annuler
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

        </TabsContent>

        <TabsContent value="planning" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <CalendarDays className="h-5 w-5 mr-2" />
                Mon planning de travail
              </CardTitle>
              <CardDescription>
                Consultez votre planning hebdomadaire défini par votre responsable
              </CardDescription>
            </CardHeader>
            <CardContent>
              <PlanningAgent
                agentId={user.id}
                agentName={`${user.prenom} ${user.nom}`}
                canEdit={false}
                refreshTrigger={planningRefreshTrigger}
              />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="historique" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <FileText className="h-5 w-5 mr-2" />
                Historique des mouvements
              </CardTitle>
              <CardDescription>
                Consultez l'historique de vos demandes et arrêts maladie
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Chargement...</p>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>Statut</TableHead>
                      <TableHead>RTT perdus</TableHead>
                      <TableHead>Solde avant</TableHead>
                      <TableHead>Solde après</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {[
                      // Convertir les demandes en format unifié
                      ...demandes.map(demande => ({
                        id: `demande-${demande.id}`,
                        type: 'demande',
                        date: demande.date_demande,
                        type_absence: demande.type_absence,
                        periode: `${demande.date_debut} - ${demande.date_fin}`,
                        duree: demande.nb_heures,
                        statut: demande.statut,
                        rtt_perdus: 0
                      })),
                      // Convertir les arrêts maladie en format unifié
                      ...arretsMaladie.map(arret => ({
                        id: `arret-${arret.id}`,
                        type: 'arret_maladie',
                        date: arret.date_creation,
                        type_absence: 'Arrêt maladie',
                        periode: `${arret.date_debut} - ${arret.date_fin}`,
                        duree: arret.nb_jours,
                        statut: 'Enregistré',
                        rtt_perdus: arret.perte_rtt
                      }))
                    ]
                      .sort((a, b) => new Date(b.date) - new Date(a.date))
                      .map((mouvement, index) => (
                      <TableRow key={mouvement.id}>
                        <TableCell>{formatDate(mouvement.date)}</TableCell>
                        <TableCell>{mouvement.type_absence}</TableCell>
                        <TableCell>
                          {formatDate(mouvement.periode.split(' - ')[0])} - {formatDate(mouvement.periode.split(' - ')[1])}
                        </TableCell>
                        <TableCell>
                          {mouvement.type === 'demande' ? 
                            (mouvement.type_absence === 'CA' ? formatDays(mouvement.duree) : formatHours(mouvement.duree)) : 
                            `${mouvement.duree} jours`}
                        </TableCell>
                        <TableCell>
                          {mouvement.type === 'demande' ? 
                            <Badge className={getStatusColor(mouvement.statut)}>
                              {mouvement.statut}
                            </Badge> : 
                            <Badge className="bg-blue-100 text-blue-800">{mouvement.statut}</Badge>}
                        </TableCell>
                        <TableCell>
                          {mouvement.rtt_perdus > 0 ? (
                            <Badge variant="destructive">{mouvement.rtt_perdus} jour(s)</Badge>
                          ) : (
                            <span className="text-gray-500">-</span>
                          )}
                        </TableCell>
                        <TableCell className="text-gray-600">
                          {mouvement.type === 'demande' ? 
                            (mouvement.type_absence === 'CA' ? 
                              formatDays(calculateSoldeAvant(mouvement.type_absence, index)) : 
                              formatHours(calculateSoldeAvant(mouvement.type_absence, index))
                            ) : '-'}
                        </TableCell>
                        <TableCell className={mouvement.type === 'demande' && mouvement.statut === 'Approuvée' ? 'text-red-600' : 'text-gray-600'}>
                          {mouvement.type === 'demande' ? 
                            (mouvement.type_absence === 'CA' ? 
                              formatDays(calculateSoldeApres(mouvement.type_absence, index)) : 
                              formatHours(calculateSoldeApres(mouvement.type_absence, index))
                            ) : '-'}
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

export default AgentDashboard


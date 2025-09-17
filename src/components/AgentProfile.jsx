import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table'
import { ArrowLeft, User, Calendar, Clock, FileText, Edit } from 'lucide-react'

const AgentProfile = ({ agentId, onBack, onEditAgent }) => {
  const [agent, setAgent] = useState(null)
  const [demandes, setDemandes] = useState([])
  const [arretsMaladie, setArretsMaladie] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (agentId) {
      fetchAgentData()
    }
  }, [agentId])

  const fetchAgentData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les données de l'agent
      const agentResponse = await fetch(`/api/agents/${agentId}`)
      if (!agentResponse.ok) {
        throw new Error('Agent non trouvé')
      }
      const agentData = await agentResponse.json()
      setAgent(agentData)

      // Récupérer les demandes de congé de l'agent
      const demandesResponse = await fetch(`/api/demandes/agent/${agentId}`)
      if (demandesResponse.ok) {
        const demandesData = await demandesResponse.json()
        setDemandes(demandesData)
      }

      // Récupérer les arrêts maladie de l'agent
      const arretsMaladieResponse = await fetch(`/api/arret-maladie?agent_id=${agentId}`, {
        credentials: 'include'
      })
      if (arretsMaladieResponse.ok) {
        const arretsMaladieData = await arretsMaladieResponse.json()
        setArretsMaladie(arretsMaladieData)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('fr-FR')
  }

  const formatHours = (hours) => {
    if (!hours) return '0.0h'
    return `${Math.round(hours * 10) / 10}h`
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

  const getStatusBadge = (status) => {
    const statusConfig = {
      'En attente': { variant: 'secondary', text: 'En attente' },
      'Approuvée': { variant: 'default', text: 'Approuvée' },
      'Refusée': { variant: 'destructive', text: 'Refusée' }
    }
    const config = statusConfig[status] || { variant: 'secondary', text: status }
    return <Badge variant={config.variant}>{config.text}</Badge>
  }

  // Fonction pour calculer le total des congés pris par type
  const calculateCongesPris = (typeAbsence) => {
    if (!demandes || !agent) return 0
    
    return demandes
      .filter(demande => demande.type_absence === typeAbsence && demande.statut === 'Approuvée')
      .reduce((total, demande) => total + (demande.nb_heures || 0), 0)
  }

  // Fonction pour calculer le solde avant une demande
  const calculateSoldeAvant = (typeAbsence, index) => {
    if (!agent) return 0
    
    const soldeInitial = getSoldeInitial(typeAbsence)
    
    // Trier toutes les demandes par date (plus ancienne en premier)
    const demandesTriees = demandes
      .filter(demande => demande.type_absence === typeAbsence && demande.statut === 'Approuvée')
      .sort((a, b) => new Date(a.date_demande) - new Date(b.date_demande))
    
    // Calculer le total des congés pris avant cette demande
    const totalPrisAvant = demandesTriees
      .slice(0, index)
      .reduce((total, demande) => total + (demande.nb_heures || 0), 0)
    
    return soldeInitial - totalPrisAvant
  }

  // Fonction pour calculer le solde après une demande
  const calculateSoldeApres = (typeAbsence, index) => {
    if (!agent) return 0
    
    const soldeInitial = getSoldeInitial(typeAbsence)
    
    // Trier toutes les demandes par date (plus ancienne en premier)
    const demandesTriees = demandes
      .filter(demande => demande.type_absence === typeAbsence && demande.statut === 'Approuvée')
      .sort((a, b) => new Date(a.date_demande) - new Date(b.date_demande))
    
    // Calculer le total des congés pris jusqu'à cette demande (inclus)
    const totalPrisJusquA = demandesTriees
      .slice(0, index + 1)
      .reduce((total, demande) => total + (demande.nb_heures || 0), 0)
    
    return soldeInitial - totalPrisJusquA
  }

  // Fonction pour calculer les RTT selon la quotité de travail
  const calculateRttFromQuotite = (quotite) => {
    if (!quotite) return 0
    
    if (quotite >= 38) {
      return 18  // 18 RTT pour 38h et plus
    } else if (quotite >= 36) {
      return 6   // 6 RTT pour 36h
    } else {
      return 0   // Pas de RTT pour moins de 36h
    }
  }

  // Fonction pour obtenir le solde initial selon le type
  const getSoldeInitial = (typeAbsence) => {
    if (!agent) return 0
    
    switch (typeAbsence) {
      case 'CA':
        return agent.solde_ca || 0
      case 'RTT':
        return calculateRttFromQuotite(agent.quotite_travail)  // Calcul automatique des RTT
      case 'CET':
        return agent.solde_cet || 0
      case 'Bonifications':
        return agent.solde_bonifications || 0
      case 'Jours de sujétions':
        return agent.solde_jours_sujetions || 0
      case 'Congés formations':
        return agent.solde_conges_formations || 0
      case 'HS':
        return agent.solde_hs || 0
      default:
        return 0
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Chargement...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">{error}</p>
        <Button onClick={onBack} variant="outline">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour
        </Button>
      </div>
    )
  }

  if (!agent) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600 mb-4">Agent non trouvé</p>
        <Button onClick={onBack} variant="outline">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header avec bouton retour */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button onClick={onBack} variant="outline" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Retour
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{agent.prenom} {agent.nom}</h1>
            <p className="text-gray-600">{agent.email}</p>
          </div>
        </div>
        <Button 
          variant="outline" 
          size="sm"
          onClick={() => onEditAgent && onEditAgent(agent)}
        >
          <Edit className="h-4 w-4 mr-2" />
          Modifier
        </Button>
      </div>

      {/* Onglets */}
      <Tabs defaultValue="informations" className="space-y-4">
        <TabsList>
          <TabsTrigger value="informations">Informations</TabsTrigger>
          <TabsTrigger value="conges">Congés</TabsTrigger>
          <TabsTrigger value="historique">Historique</TabsTrigger>
        </TabsList>

        {/* Onglet Informations */}
        <TabsContent value="informations" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Informations personnelles */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <User className="h-5 w-5 mr-2" />
                  Informations personnelles
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-500">Nom complet</label>
                  <p className="text-sm">{agent.prenom} {agent.nom}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Email</label>
                  <p className="text-sm">{agent.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Rôle</label>
                  <p className="text-sm">{agent.role}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Service</label>
                  <p className="text-sm">{agent.service?.nom_service || 'Non assigné'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Date d'entrée</label>
                  <p className="text-sm">{formatDate(agent.date_debut_contrat)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Quotité de travail</label>
                  <p className="text-sm">{agent.quotite_travail}h/semaine</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Année d'entrée FP</label>
                  <p className="text-sm">{agent.annee_entree_fp || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Date de fin de contrat</label>
                  <p className="text-sm">{formatDate(agent.date_fin_contrat)}</p>
                </div>
              </CardContent>
            </Card>

            {/* Soldes initiaux */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Clock className="h-5 w-5 mr-2" />
                  Soldes initiaux
                </CardTitle>
                <CardDescription>
                  Droits initiaux accordés (les calculs de consommation sont dans l'historique)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde CA</label>
                  <p className="text-sm font-semibold text-blue-600">{agent.solde_ca || 0} jours</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde RTT</label>
                  <p className="text-sm font-semibold text-blue-600">{calculateRttFromQuotite(agent.quotite_travail)} jours</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde CET</label>
                  <p className="text-sm font-semibold text-blue-600">{agent.solde_cet || 0} jours</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde HS</label>
                  <p className="text-sm font-semibold text-blue-600">{agent.solde_hs || 0} jours</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde Bonifications</label>
                  <p className="text-sm font-semibold text-blue-600">{agent.solde_bonifications || 0} jours</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde Jours de sujétions</label>
                  <p className="text-sm font-semibold text-blue-600">{agent.solde_jours_sujetions || 0} jours</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Solde Congés formations</label>
                  <p className="text-sm font-semibold text-blue-600">{agent.solde_conges_formations || 0} jours</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Onglet Congés */}
        <TabsContent value="conges" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calendar className="h-5 w-5 mr-2" />
                Demandes de congé
              </CardTitle>
              <CardDescription>
                Historique des demandes de congé de {agent.prenom} {agent.nom}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {demandes.length === 0 ? (
                <p className="text-gray-500 text-center py-4">Aucune demande de congé</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Type</TableHead>
                      <TableHead>Période</TableHead>
                      <TableHead>Durée</TableHead>
                      <TableHead>Date demande</TableHead>
                      <TableHead>Statut</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {demandes.map((demande) => (
                      <TableRow key={demande.id}>
                        <TableCell>{demande.type_conge}</TableCell>
                        <TableCell>
                          {formatDate(demande.date_debut)} - {formatDate(demande.date_fin)}
                        </TableCell>
                        <TableCell>{formatHours(demande.nb_heures)}</TableCell>
                        <TableCell>{formatDate(demande.date_demande)}</TableCell>
                        <TableCell>{getStatusBadge(demande.statut)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet Historique */}
        <TabsContent value="historique" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <FileText className="h-5 w-5 mr-2" />
                Historique des congés et soldes
              </CardTitle>
              <CardDescription>
                Droits totaux et historique des mouvements de {agent.prenom} {agent.nom}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Tableau des droits totaux */}
                <div>
                  <h3 className="text-lg font-semibold mb-4">Droits totaux accordés</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Type de congé</TableHead>
                        <TableHead>Droits accordés</TableHead>
                        <TableHead>Congés pris</TableHead>
                        <TableHead>Solde restant</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      <TableRow className="font-medium">
                        <TableCell>Congés Annuels (CA)</TableCell>
                        <TableCell>{formatSolde('CA', agent.solde_ca)}</TableCell>
                        <TableCell>{formatSolde('CA', calculateCongesPris('CA'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('CA', agent.solde_ca - calculateCongesPris('CA'))}
                        </TableCell>
                      </TableRow>
                      <TableRow className="font-medium">
                        <TableCell>RTT</TableCell>
                        <TableCell>{formatSolde('RTT', agent.solde_rtt)}</TableCell>
                        <TableCell>{formatSolde('RTT', calculateCongesPris('RTT'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('RTT', agent.solde_rtt - calculateCongesPris('RTT'))}
                        </TableCell>
                      </TableRow>
                      <TableRow className="font-medium">
                        <TableCell>Compte Épargne Temps (CET)</TableCell>
                        <TableCell>{formatSolde('CET', agent.solde_cet)}</TableCell>
                        <TableCell>{formatSolde('CET', calculateCongesPris('CET'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('CET', agent.solde_cet - calculateCongesPris('CET'))}
                        </TableCell>
                      </TableRow>
                      <TableRow className="font-medium">
                        <TableCell>Bonifications</TableCell>
                        <TableCell>{formatSolde('Bonifications', agent.solde_bonifications)}</TableCell>
                        <TableCell>{formatSolde('Bonifications', calculateCongesPris('Bonifications'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('Bonifications', agent.solde_bonifications - calculateCongesPris('Bonifications'))}
                        </TableCell>
                      </TableRow>
                      <TableRow className="font-medium">
                        <TableCell>Jours de sujétions</TableCell>
                        <TableCell>{formatSolde('Jours de sujétions', agent.solde_jours_sujetions)}</TableCell>
                        <TableCell>{formatSolde('Jours de sujétions', calculateCongesPris('Jours de sujétions'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('Jours de sujétions', agent.solde_jours_sujetions - calculateCongesPris('Jours de sujétions'))}
                        </TableCell>
                      </TableRow>
                      <TableRow className="font-medium">
                        <TableCell>Congés formations</TableCell>
                        <TableCell>{formatSolde('Congés formations', agent.solde_conges_formations)}</TableCell>
                        <TableCell>{formatSolde('Congés formations', calculateCongesPris('Congés formations'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('Congés formations', agent.solde_conges_formations - calculateCongesPris('Congés formations'))}
                        </TableCell>
                      </TableRow>
                      <TableRow className="font-medium">
                        <TableCell>Heures Supplémentaires (HS)</TableCell>
                        <TableCell>{formatSolde('HS', agent.solde_hs)}</TableCell>
                        <TableCell>{formatSolde('HS', calculateCongesPris('HS'))}</TableCell>
                        <TableCell className="text-green-600 font-bold">
                          {formatSolde('HS', agent.solde_hs - calculateCongesPris('HS'))}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </div>

                {/* Historique détaillé des mouvements */}
                <div>
                  <h3 className="text-lg font-semibold mb-4">Historique des mouvements</h3>
                  {demandes.length === 0 && arretsMaladie.length === 0 ? (
                    <p className="text-gray-500 text-center py-4">Aucun mouvement enregistré</p>
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
                        {(() => {
                          // Créer la liste des mouvements
                          const mouvements = [
                            // Convertir les demandes en format unifié
                            ...demandes.map(demande => ({
                              id: demande.id,
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
                          ].sort((a, b) => new Date(a.date) - new Date(b.date)) // Plus ancienne en haut
                          
                          // Calculer les soldes pour chaque type d'absence
                          const soldesParType = {}
                          const typesAbsence = [...new Set(mouvements.map(m => m.type_absence))]
                          
                          typesAbsence.forEach(type => {
                            const demandesType = demandes
                              .filter(d => d.type_absence === type && d.statut === 'Approuvée')
                              .sort((a, b) => new Date(a.date_demande) - new Date(b.date_demande))
                            
                            soldesParType[type] = {
                              initial: getSoldeInitial(type),
                              calcules: []
                            }
                            
                            let soldeActuel = soldesParType[type].initial
                            demandesType.forEach((demande, index) => {
                              soldesParType[type].calcules.push({
                                avant: soldeActuel,
                                apres: soldeActuel - demande.nb_heures
                              })
                              soldeActuel -= demande.nb_heures
                            })
                          })
                          
                          return mouvements.map((mouvement, index) => {
                            let soldeInfo = null
                            
                            if (mouvement.type === 'demande' && mouvement.statut === 'Approuvée') {
                              const demandesType = demandes
                                .filter(d => d.type_absence === mouvement.type_absence && d.statut === 'Approuvée')
                                .sort((a, b) => new Date(a.date_demande) - new Date(b.date_demande))
                              
                              const demandeIndex = demandesType.findIndex(d => d.id === mouvement.id)
                              if (demandeIndex !== -1 && soldesParType[mouvement.type_absence]) {
                                soldeInfo = soldesParType[mouvement.type_absence].calcules[demandeIndex]
                              }
                            }
                            
                            return (
                          <TableRow key={mouvement.id}>
                            <TableCell>{formatDate(mouvement.date)}</TableCell>
                            <TableCell>{mouvement.type_absence}</TableCell>
                            <TableCell>
                              {formatDate(mouvement.periode.split(' - ')[0])} - {formatDate(mouvement.periode.split(' - ')[1])}
                            </TableCell>
                            <TableCell>
                              {mouvement.type === 'demande' ? formatHours(mouvement.duree) : `${mouvement.duree} jours`}
                            </TableCell>
                            <TableCell>
                              {mouvement.type === 'demande' ? getStatusBadge(mouvement.statut) : 
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
                              {mouvement.type === 'demande' && soldeInfo ? formatHours(soldeInfo.avant) : '-'}
                            </TableCell>
                            <TableCell className={mouvement.type === 'demande' && mouvement.statut === 'Approuvée' ? 'text-red-600' : 'text-gray-600'}>
                              {mouvement.type === 'demande' && soldeInfo ? formatHours(soldeInfo.apres) : '-'}
                            </TableCell>
                          </TableRow>
                            )
                          })
                        })()}
                      </TableBody>
                    </Table>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AgentProfile

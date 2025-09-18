import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon, Plus, Edit, Trash2, Users, TrendingUp } from 'lucide-react'
import api from '../services/api'

const Calendar = ({ user }) => {
  const [currentSemaine, setCurrentSemaine] = useState('')
  const [calendrierData, setCalendrierData] = useState(null)
  const [statistiques, setStatistiques] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showPresenceForm, setShowPresenceForm] = useState(false)
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [selectedDate, setSelectedDate] = useState('')
  const [editingPresence, setEditingPresence] = useState(null)
  const [presenceForm, setPresenceForm] = useState({
    agent_id: '',
    date_presence: '',
    creneau: 'matin',
    statut: 'present',
    motif: '',
    heure_debut: '',
    heure_fin: ''
  })

  // Initialiser avec la semaine courante
  useEffect(() => {
    const today = new Date()
    const semaine = getSemaineCourante(today)
    setCurrentSemaine(semaine)
    fetchCalendrier(semaine)
    fetchStatistiques(semaine)
  }, [])

  const getSemaineCourante = (date) => {
    const startOfYear = new Date(date.getFullYear(), 0, 1)
    const days = Math.floor((date - startOfYear) / (24 * 60 * 60 * 1000))
    const weekNumber = Math.ceil((days + startOfYear.getDay() + 1) / 7)
    return `${date.getFullYear()}-${weekNumber.toString().padStart(2, '0')}`
  }

  const getDateFromSemaine = (semaine) => {
    const [annee, semaineNum] = semaine.split('-')
    const date = new Date(parseInt(annee), 0, 1)
    const daysToAdd = (parseInt(semaineNum) - 1) * 7
    date.setDate(date.getDate() + daysToAdd)
    
    // Ajuster pour que le lundi soit le premier jour
    const dayOfWeek = date.getDay()
    const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek
    date.setDate(date.getDate() + mondayOffset)
    
    return date
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', { 
      weekday: 'short', 
      day: 'numeric', 
      month: 'short' 
    })
  }

  const getStatutColor = (statut, isDemande = false) => {
    const colors = {
      present: 'bg-green-100 text-green-800 border-green-200',
      absent: 'bg-red-100 text-red-800 border-red-200',
      conges: isDemande ? 'bg-blue-200 text-blue-900 border-blue-300' : 'bg-blue-100 text-blue-800 border-blue-200',
      maladie: 'bg-orange-100 text-orange-800 border-orange-200',
      rtt: isDemande ? 'bg-purple-200 text-purple-900 border-purple-300' : 'bg-purple-100 text-purple-800 border-purple-200',
      partiel: 'bg-yellow-100 text-yellow-800 border-yellow-200'
    }
    return colors[statut] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  const getStatutLabel = (statut, isDemande = false) => {
    const labels = {
      present: 'Présent',
      absent: 'Absent',
      conges: isDemande ? 'Congés ✓' : 'Congés',
      maladie: 'Maladie',
      rtt: isDemande ? 'RTT ✓' : 'RTT',
      partiel: 'Partiel'
    }
    return labels[statut] || statut
  }

  const fetchCalendrier = async (semaine) => {
    setLoading(true)
    try {
      const response = await api.getPresenceCalendrier(semaine)
      if (response.ok) {
        const data = await response.json()
        setCalendrierData(data)
      } else {
        console.error('Erreur lors du chargement du calendrier')
      }
    } catch (err) {
      console.error('Erreur:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchStatistiques = async (semaine) => {
    try {
      const response = await api.getPresenceStatistiques(semaine)
      if (response.ok) {
        const data = await response.json()
        setStatistiques(data)
      }
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err)
    }
  }

  const handleSemaineChange = (direction) => {
    const [annee, semaineNum] = currentSemaine.split('-')
    let newAnnee = parseInt(annee)
    let newSemaine = parseInt(semaineNum)
    
    if (direction === 'prev') {
      newSemaine -= 1
      if (newSemaine < 1) {
        newSemaine = 52
        newAnnee -= 1
      }
    } else {
      newSemaine += 1
      if (newSemaine > 52) {
        newSemaine = 1
        newAnnee += 1
      }
    }
    
    const nouvelleSemaine = `${newAnnee}-${newSemaine.toString().padStart(2, '0')}`
    setCurrentSemaine(nouvelleSemaine)
    fetchCalendrier(nouvelleSemaine)
    fetchStatistiques(nouvelleSemaine)
  }

  const handleAddPresence = (agentId, date, creneau) => {
    setSelectedAgent(agentId)
    setSelectedDate(date)
    setPresenceForm({
      agent_id: agentId.toString(),
      date_presence: date,
      creneau: creneau,
      statut: 'present',
      motif: '',
      heure_debut: creneau === 'matin' ? '08:00' : '13:00',
      heure_fin: creneau === 'matin' ? '12:00' : '17:00'
    })
    setEditingPresence(null)
    setShowPresenceForm(true)
  }

  const handleEditPresence = (presence) => {
    setEditingPresence(presence)
    setPresenceForm({
      agent_id: presence.agent_id.toString(),
      date_presence: presence.date_presence,
      creneau: presence.creneau || 'matin',
      statut: presence.statut,
      motif: presence.motif || '',
      heure_debut: presence.heure_debut || '08:00',
      heure_fin: presence.heure_fin || '17:00'
    })
    setShowPresenceForm(true)
  }

  const handlePresenceSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = editingPresence 
        ? await api.updatePresence(editingPresence.id, presenceForm)
        : await api.createPresence(presenceForm)

      if (response.ok) {
        await fetchCalendrier(currentSemaine)
        await fetchStatistiques(currentSemaine)
        setShowPresenceForm(false)
        setEditingPresence(null)
      } else {
        const data = await response.json()
        alert(data.error || 'Erreur lors de la sauvegarde')
      }
    } catch (err) {
      alert('Erreur de connexion au serveur')
    }
  }

  const handleDeletePresence = async (presenceId) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette présence ?')) {
      try {
        const response = await api.deletePresence(presenceId)

        if (response.ok) {
          await fetchCalendrier(currentSemaine)
          await fetchStatistiques(currentSemaine)
        } else {
          const data = await response.json()
          alert(data.error || 'Erreur lors de la suppression')
        }
      } catch (err) {
        alert('Erreur de connexion au serveur')
      }
    }
  }

  if (!calendrierData) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du calendrier...</p>
        </div>
      </div>
    )
  }

  const joursSemaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
  const dateDebut = new Date(calendrierData.date_debut)

  return (
    <div className="space-y-6">
      {/* Header avec navigation et statistiques */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="flex items-center gap-2">
                <CalendarIcon className="h-6 w-6 text-blue-600" />
                Calendrier de présence - Semaine {currentSemaine}
              </CardTitle>
              <CardDescription>
                {formatDate(calendrierData.date_debut)} - {formatDate(calendrierData.date_fin)}
              </CardDescription>
            </div>
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSemaineChange('prev')}
                className="flex items-center gap-2"
              >
                <ChevronLeft className="h-4 w-4" />
                Semaine précédente
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const semaine = getSemaineCourante(new Date())
                  setCurrentSemaine(semaine)
                  fetchCalendrier(semaine)
                  fetchStatistiques(semaine)
                }}
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                Aujourd'hui
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSemaineChange('next')}
                className="flex items-center gap-2"
              >
                Semaine suivante
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {statistiques && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-xl border border-blue-200">
                <div className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-blue-600" />
                  <span className="font-semibold text-blue-800">Agents</span>
                </div>
                <p className="text-2xl font-bold text-blue-900">{statistiques.total_agents}</p>
              </div>
              <div className="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-xl border border-green-200">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span className="font-semibold text-green-800">Présence</span>
                </div>
                <p className="text-2xl font-bold text-green-900">{statistiques.pourcentage_presence}%</p>
              </div>
              <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-xl border border-purple-200">
                <div className="flex items-center gap-2">
                  <CalendarIcon className="h-5 w-5 text-purple-600" />
                  <span className="font-semibold text-purple-800">Total entrées</span>
                </div>
                <p className="text-2xl font-bold text-purple-900">{statistiques.presences_totales}</p>
              </div>
              <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-4 rounded-xl border border-orange-200">
                <div className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-orange-600" />
                  <span className="font-semibold text-orange-800">Jours possibles</span>
                </div>
                <p className="text-2xl font-bold text-orange-900">{statistiques.total_jours_possibles}</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Calendrier */}
      <Card>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left p-4 font-bold text-gray-700 bg-gradient-to-r from-gray-50 to-gray-100 w-48">Agent</th>
                  {joursSemaine.map((jour, index) => {
                    const date = new Date(dateDebut)
                    date.setDate(dateDebut.getDate() + index)
                    return (
                      <th key={index} className="text-center p-2 font-bold text-gray-700 bg-gradient-to-r from-gray-50 to-gray-100">
                        <div>{jour}</div>
                        <div className="text-sm font-normal text-gray-500">{date.getDate()}</div>
                        <div className="text-xs text-gray-400 mt-1">
                          <div className="border-b border-gray-300 pb-1 mb-1">Matin</div>
                          <div>Après-midi</div>
                        </div>
                      </th>
                    )
                  })}
                </tr>
              </thead>
              <tbody>
                {calendrierData.agents.map((agent) => (
                  <tr key={agent.id} className="border-b border-gray-100 hover:bg-gray-50/50">
                    <td className="p-4 font-medium text-gray-900">
                      <div>
                        <div className="font-semibold">{agent.nom}</div>
                        <div className="text-sm text-gray-500">{agent.service}</div>
                      </div>
                    </td>
                    {joursSemaine.map((jour, index) => {
                      const date = new Date(dateDebut)
                      date.setDate(dateDebut.getDate() + index)
                      const dateStr = date.toISOString().split('T')[0]
                      const jourData = agent.jours[dateStr]
                      
                      return (
                        <td key={index} className="p-1 text-center align-top">
                          <div className="space-y-1">
                            {/* Créneau Matin */}
                            <div className="h-8 flex items-center justify-center">
                              {jourData && jourData.matin && jourData.matin.presence ? (
                                <div className="relative group w-full">
                                  <Badge className={`${getStatutColor(jourData.matin.statut, jourData.matin.presence.is_demande)} cursor-pointer text-xs px-2 py-1`}>
                                    {getStatutLabel(jourData.matin.statut, jourData.matin.presence.is_demande)}
                                  </Badge>
                                  {!jourData.matin.presence.is_demande && (
                                    <div className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity">
                                      <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => handleEditPresence(jourData.matin.presence)}
                                        className="h-5 w-5 p-0"
                                      >
                                        <Edit className="h-2 w-2" />
                                      </Button>
                                    </div>
                                  )}
                                </div>
                              ) : (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => handleAddPresence(agent.id, dateStr, 'matin')}
                                  className="h-6 w-full text-gray-400 hover:text-gray-600 border-dashed text-xs"
                                >
                                  <Plus className="h-3 w-3" />
                                </Button>
                              )}
                            </div>
                            
                            {/* Créneau Après-midi */}
                            <div className="h-8 flex items-center justify-center">
                              {jourData && jourData.apres_midi && jourData.apres_midi.presence ? (
                                <div className="relative group w-full">
                                  <Badge className={`${getStatutColor(jourData.apres_midi.statut, jourData.apres_midi.presence.is_demande)} cursor-pointer text-xs px-2 py-1`}>
                                    {getStatutLabel(jourData.apres_midi.statut, jourData.apres_midi.presence.is_demande)}
                                  </Badge>
                                  {!jourData.apres_midi.presence.is_demande && (
                                    <div className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity">
                                      <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => handleEditPresence(jourData.apres_midi.presence)}
                                        className="h-5 w-5 p-0"
                                      >
                                        <Edit className="h-2 w-2" />
                                      </Button>
                                    </div>
                                  )}
                                </div>
                              ) : (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => handleAddPresence(agent.id, dateStr, 'apres_midi')}
                                  className="h-6 w-full text-gray-400 hover:text-gray-600 border-dashed text-xs"
                                >
                                  <Plus className="h-3 w-3" />
                                </Button>
                              )}
                            </div>
                          </div>
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Légende */}
      <Card>
        <CardContent className="p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Légende des statuts</h4>
          <div className="space-y-3">
            <div className="flex flex-wrap gap-3">
              <Badge className={getStatutColor('present')}>Présent</Badge>
              <Badge className={getStatutColor('absent')}>Absent</Badge>
              <Badge className={getStatutColor('maladie')}>Maladie</Badge>
              <Badge className={getStatutColor('partiel')}>Partiel</Badge>
            </div>
            <div className="flex flex-wrap gap-3">
              <Badge className={getStatutColor('conges')}>Congés manuels</Badge>
              <Badge className={getStatutColor('conges', true)}>Congés ✓</Badge>
              <Badge className={getStatutColor('rtt')}>RTT manuels</Badge>
              <Badge className={getStatutColor('rtt', true)}>RTT ✓</Badge>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              <strong>✓</strong> = Demandes de congés validées automatiquement affichées
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Formulaire de présence */}
      <Dialog open={showPresenceForm}>
        <DialogContent onClose={() => setShowPresenceForm(false)}>
          <DialogHeader onClose={() => setShowPresenceForm(false)}>
            <DialogTitle>
              {editingPresence ? 'Modifier la présence' : 'Ajouter une présence'}
            </DialogTitle>
            <DialogDescription>
              {editingPresence ? 'Modifiez les informations de présence' : 'Enregistrez la présence de l\'agent'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handlePresenceSubmit} className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="date_presence">Date</Label>
                <Input
                  id="date_presence"
                  type="date"
                  value={presenceForm.date_presence}
                  onChange={(e) => setPresenceForm({...presenceForm, date_presence: e.target.value})}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="creneau">Créneau</Label>
                <Select
                  value={presenceForm.creneau}
                  onValueChange={(value) => setPresenceForm({...presenceForm, creneau: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner un créneau" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="matin">Matin</SelectItem>
                    <SelectItem value="apres_midi">Après-midi</SelectItem>
                    <SelectItem value="journee">Journée complète</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="statut">Statut</Label>
                <Select
                  value={presenceForm.statut}
                  onValueChange={(value) => setPresenceForm({...presenceForm, statut: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner un statut" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="present">Présent</SelectItem>
                    <SelectItem value="absent">Absent</SelectItem>
                    <SelectItem value="conges">Congés</SelectItem>
                    <SelectItem value="maladie">Maladie</SelectItem>
                    <SelectItem value="rtt">RTT</SelectItem>
                    <SelectItem value="partiel">Présence partielle</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            {presenceForm.statut === 'partiel' && (
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="heure_debut">Heure de début</Label>
                  <Input
                    id="heure_debut"
                    type="time"
                    value={presenceForm.heure_debut}
                    onChange={(e) => setPresenceForm({...presenceForm, heure_debut: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="heure_fin">Heure de fin</Label>
                  <Input
                    id="heure_fin"
                    type="time"
                    value={presenceForm.heure_fin}
                    onChange={(e) => setPresenceForm({...presenceForm, heure_fin: e.target.value})}
                  />
                </div>
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="motif">Motif (optionnel)</Label>
              <Textarea
                id="motif"
                placeholder="Décrivez le motif de l'absence ou de la présence partielle..."
                value={presenceForm.motif}
                onChange={(e) => setPresenceForm({...presenceForm, motif: e.target.value})}
                rows={3}
              />
            </div>
            
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={() => setShowPresenceForm(false)}>
                Annuler
              </Button>
              <Button type="submit">
                {editingPresence ? 'Modifier' : 'Enregistrer'}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default Calendar

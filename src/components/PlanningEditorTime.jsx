import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { Clock, Calendar, Save, X, Plus, Trash2, Edit } from 'lucide-react'
import api from '../services/api'

const PlanningEditorTime = ({ agentId, agentName, onSave, onCancel }) => {
  const [plannings, setPlannings] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [selectedJour, setSelectedJour] = useState(null)
  const [showJourDialog, setShowJourDialog] = useState(false)

  const jours = [
    { value: 0, label: 'Lundi' },
    { value: 1, label: 'Mardi' },
    { value: 2, label: 'Mercredi' },
    { value: 3, label: 'Jeudi' },
    { value: 4, label: 'Vendredi' },
    { value: 5, label: 'Samedi' }
  ]

  useEffect(() => {
    fetchPlanning()
  }, [agentId])

  const fetchPlanning = async () => {
    try {
      setLoading(true)
      const response = await api.getPlanningAgent(agentId)
      
      if (response.ok) {
        const data = await response.json()
        setPlannings(data.planning || {})
      }
    } catch (err) {
      console.error('Erreur lors du chargement du planning:', err)
    } finally {
      setLoading(false)
    }
  }

  const initializeJour = (jour) => {
    if (!plannings[jour]) {
      setPlannings(prev => ({
        ...prev,
        [jour]: {
          jour_nom: jours[jour].label,
          plannings: [],
          creneaux: []
        }
      }))
    }
  }

  const handleEditJour = (jour) => {
    initializeJour(jour)
    setSelectedJour(jour)
    setShowJourDialog(true)
  }

  const handleSaveJour = (jourData) => {
    // Mettre à jour le planning local avec les nouvelles données
    setPlannings(prev => ({
      ...prev,
      [selectedJour]: {
        jour_nom: jours[selectedJour].label,
        plannings: [jourData],
        creneaux: []
      }
    }))
    setShowJourDialog(false)
  }

  const handleDeleteJour = (jour) => {
    setPlannings(prev => {
      const newPlannings = { ...prev }
      delete newPlannings[jour]
      return newPlannings
    })
  }

  const handleSaveAll = async () => {
    try {
      setSaving(true)
      
      // Préparer les données pour l'API
      const planningsData = Object.entries(plannings).map(([jour, data]) => {
        if (data.plannings && data.plannings.length > 0) {
          return {
            jour_semaine: parseInt(jour),
            heure_debut: data.plannings[0].heure_debut,
            heure_fin: data.plannings[0].heure_fin,
            pause_debut: data.plannings[0].pause_debut || null,
            pause_fin: data.plannings[0].pause_fin || null
          }
        }
        return null
      }).filter(Boolean)

      console.log('Données à envoyer:', planningsData)

      const response = await api.savePlanningAgent(agentId, {
        plannings: planningsData
      })

      console.log('Réponse API:', response.status)

      if (response.ok) {
        const result = await response.json()
        console.log('Résultat sauvegarde:', result)
        alert('Planning sauvegardé avec succès!')
        onSave()
      } else {
        const error = await response.json()
        console.error('Erreur API:', error)
        alert('Erreur lors de la sauvegarde: ' + error.error)
      }
    } catch (err) {
      console.error('Erreur de connexion:', err)
      alert('Erreur de connexion: ' + err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Édition du planning - {agentName}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Chargement...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Édition du planning - {agentName}
          </CardTitle>
          <CardDescription>
            Configurez les horaires de travail pour chaque jour de la semaine
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {jours.map((jour) => (
              <div key={jour.value} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-lg">{jour.label}</h3>
                  <div className="flex space-x-2">
                    <Button
                      onClick={() => handleEditJour(jour.value)}
                      variant="outline"
                      size="sm"
                    >
                      <Edit className="h-4 w-4 mr-2" />
                      {plannings[jour.value]?.plannings?.length > 0 ? 'Modifier' : 'Définir'}
                    </Button>
                    {plannings[jour.value]?.plannings?.length > 0 && (
                      <Button
                        onClick={() => handleDeleteJour(jour.value)}
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
                
                {plannings[jour.value]?.plannings?.length > 0 ? (
                  <div className="bg-gray-50 p-3 rounded">
                    <div className="flex items-center space-x-4">
                      <Badge variant="outline">
                        <Clock className="h-3 w-3 mr-1" />
                        {plannings[jour.value].plannings[0].heure_debut} - {plannings[jour.value].plannings[0].heure_fin}
                      </Badge>
                      {plannings[jour.value].plannings[0].pause_debut && plannings[jour.value].plannings[0].pause_fin && (
                        <Badge variant="outline" className="bg-orange-50 text-orange-700">
                          Pause: {plannings[jour.value].plannings[0].pause_debut} - {plannings[jour.value].plannings[0].pause_fin}
                        </Badge>
                      )}
                      <Badge variant="outline" className="bg-green-50 text-green-700">
                        {plannings[jour.value].plannings[0].duree_travail}h
                      </Badge>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    Aucun horaire défini
                  </div>
                )}
              </div>
            ))}
          </div>
          
          <div className="flex justify-end space-x-2 mt-6">
            <Button onClick={onCancel} variant="outline">
              <X className="h-4 w-4 mr-2" />
              Annuler
            </Button>
            <Button onClick={handleSaveAll} disabled={saving}>
              <Save className="h-4 w-4 mr-2" />
              {saving ? 'Sauvegarde...' : 'Sauvegarder'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Dialog pour éditer un jour */}
      <Dialog open={showJourDialog} onOpenChange={setShowJourDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>
              {selectedJour !== null && `Planning du ${jours[selectedJour]?.label}`}
            </DialogTitle>
            <DialogDescription>
              Définissez les horaires de travail et les pauses
            </DialogDescription>
          </DialogHeader>
          
          {selectedJour !== null && (
            <JourPlanningFormTime
              jour={selectedJour}
              jourLabel={jours[selectedJour]?.label}
              planning={plannings[selectedJour]}
              onSave={handleSaveJour}
              onCancel={() => setShowJourDialog(false)}
            />
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}

const JourPlanningFormTime = ({ jour, jourLabel, planning, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    heure_debut: '08:00',
    heure_fin: '17:00',
    pause_debut: '',
    pause_fin: '',
    actif: true
  })

  useEffect(() => {
    if (planning?.plannings?.length > 0) {
      const p = planning.plannings[0]
      setFormData({
        heure_debut: p.heure_debut || '08:00',
        heure_fin: p.heure_fin || '17:00',
        pause_debut: p.pause_debut || '',
        pause_fin: p.pause_fin || '',
        actif: true
      })
    }
  }, [planning])

  const calculerDuree = () => {
    const debut = new Date(`2000-01-01T${formData.heure_debut}`)
    const fin = new Date(`2000-01-01T${formData.heure_fin}`)
    let duree = (fin - debut) / (1000 * 60 * 60) // en heures
    
    if (formData.pause_debut && formData.pause_fin) {
      const pauseDebut = new Date(`2000-01-01T${formData.pause_debut}`)
      const pauseFin = new Date(`2000-01-01T${formData.pause_fin}`)
      const dureePause = (pauseFin - pauseDebut) / (1000 * 60 * 60)
      duree -= dureePause
    }
    
    return Math.max(0, duree).toFixed(1)
  }

  const handleSave = () => {
    // Calculer la durée de travail
    const duree = calculerDuree()
    
    // Créer l'objet de données du jour
    const jourData = {
      jour_semaine: jour,
      heure_debut: formData.heure_debut,
      heure_fin: formData.heure_fin,
      pause_debut: formData.pause_debut || null,
      pause_fin: formData.pause_fin || null,
      duree_travail: parseFloat(duree),
      actif: formData.actif
    }
    
    onSave(jourData)
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="heure_debut">Heure de début</Label>
          <Input
            id="heure_debut"
            type="time"
            value={formData.heure_debut}
            onChange={(e) => setFormData(prev => ({ ...prev, heure_debut: e.target.value }))}
            className="w-full"
          />
        </div>
        
        <div>
          <Label htmlFor="heure_fin">Heure de fin</Label>
          <Input
            id="heure_fin"
            type="time"
            value={formData.heure_fin}
            onChange={(e) => setFormData(prev => ({ ...prev, heure_fin: e.target.value }))}
            className="w-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="pause_debut">Début de pause (optionnel)</Label>
          <Input
            id="pause_debut"
            type="time"
            value={formData.pause_debut}
            onChange={(e) => setFormData(prev => ({ ...prev, pause_debut: e.target.value }))}
            className="w-full"
          />
        </div>
        
        <div>
          <Label htmlFor="pause_fin">Fin de pause</Label>
          <Input
            id="pause_fin"
            type="time"
            value={formData.pause_fin}
            onChange={(e) => setFormData(prev => ({ ...prev, pause_fin: e.target.value }))}
            disabled={!formData.pause_debut}
            className="w-full"
          />
        </div>
      </div>

      <div className="bg-gray-50 p-3 rounded">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">Durée de travail:</span>
          <Badge variant="outline" className="bg-green-50 text-green-700">
            {calculerDuree()}h
          </Badge>
        </div>
      </div>

      <div className="flex justify-end space-x-2">
        <Button onClick={onCancel} variant="outline">
          Annuler
        </Button>
        <Button onClick={handleSave}>
          Sauvegarder
        </Button>
      </div>
    </div>
  )
}

export default PlanningEditorTime

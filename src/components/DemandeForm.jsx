import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ArrowLeft, Loader2 } from 'lucide-react'

const DemandeForm = ({ user, onCancel, onSuccess }) => {
  const [formData, setFormData] = useState({
    type_absence: '',
    date_debut: '',
    date_fin: '',
    demi_journees: '',
    motif: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Fonctions de formatage des unités
  const formatDays = (days) => {
    if (!days) return '0 jour'
    if (days === 1) return '1 jour'
    if (days === 0.5) return '0.5 jour'
    return `${Math.round(days * 10) / 10} jours`
  }

  const formatHours = (hours) => {
    if (!hours) return '0h'
    return `${Math.round(hours * 10) / 10}h`
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

  const typesAbsence = [
    { value: 'CA', label: 'Congés Annuels', solde: user.solde_ca },
    { value: 'RTT', label: 'RTT', solde: calculateRttFromQuotite(user.quotite_travail) },
    { value: 'CET', label: 'Compte Épargne Temps', solde: user.solde_cet },
    { value: 'Bonifications', label: 'Bonifications', solde: user.solde_bonifications },
    { value: 'Jours de sujétions', label: 'Jours de sujétions', solde: user.solde_jours_sujetions },
    { value: 'Congés formations', label: 'Congés formations', solde: user.solde_conges_formations },
    { value: 'HS', label: 'Heures Supplémentaires', solde: user.solde_hs }
  ]

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Validation basique
    if (!formData.type_absence || !formData.date_debut || !formData.date_fin) {
      setError('Veuillez remplir tous les champs obligatoires')
      setLoading(false)
      return
    }

    if (new Date(formData.date_debut) > new Date(formData.date_fin)) {
      setError('La date de début doit être antérieure à la date de fin')
      setLoading(false)
      return
    }

    try {
      const response = await fetch('/api/demandes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (response.ok) {
        onSuccess()
      } else {
        setError(data.error || 'Erreur lors de la création de la demande')
      }
    } catch (err) {
      setError('Erreur de connexion au serveur')
    } finally {
      setLoading(false)
    }
  }

  const getSelectedTypeSolde = () => {
    const selectedType = typesAbsence.find(type => type.value === formData.type_absence)
    return selectedType ? selectedType.solde : 0
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="outline" size="sm" onClick={onCancel}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour
        </Button>
        <h2 className="text-2xl font-bold">Nouvelle demande de congé</h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Détails de la demande</CardTitle>
          <CardDescription>
            Remplissez les informations pour votre demande de congé ou RTT
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="type_absence">Type d'absence *</Label>
                <Select
                  value={formData.type_absence}
                  onValueChange={(value) => handleInputChange('type_absence', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionnez le type d'absence">
                      {formData.type_absence ? 
                        typesAbsence.find(type => type.value === formData.type_absence)?.label + 
                        ` (Solde: ${formatSolde(formData.type_absence, typesAbsence.find(type => type.value === formData.type_absence)?.solde)})` 
                        : null
                      }
                    </SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    {typesAbsence.map((type) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label} (Solde: {formatSolde(type.value, type.solde)})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {formData.type_absence && (
                  <p className="text-sm text-muted-foreground">
                    Solde disponible: {formatSolde(formData.type_absence, getSelectedTypeSolde())}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="demi_journees">Demi-journées</Label>
                <Select
                  value={formData.demi_journees}
                  onValueChange={(value) => handleInputChange('demi_journees', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Journée complète">
                      {formData.demi_journees === '' ? 'Journée complète' :
                       formData.demi_journees === 'matin' ? 'Matin uniquement' :
                       formData.demi_journees === 'après-midi' ? 'Après-midi uniquement' : null}
                    </SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">Journée complète</SelectItem>
                    <SelectItem value="matin">Matin uniquement</SelectItem>
                    <SelectItem value="après-midi">Après-midi uniquement</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="date_debut">Date de début *</Label>
                <Input
                  id="date_debut"
                  type="date"
                  value={formData.date_debut}
                  onChange={(e) => handleInputChange('date_debut', e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="date_fin">Date de fin *</Label>
                <Input
                  id="date_fin"
                  type="date"
                  value={formData.date_fin}
                  onChange={(e) => handleInputChange('date_fin', e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="motif">Motif (optionnel)</Label>
              <Textarea
                id="motif"
                placeholder="Précisez le motif de votre demande..."
                value={formData.motif}
                onChange={(e) => handleInputChange('motif', e.target.value)}
                rows={3}
              />
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="flex justify-end space-x-4">
              <Button type="button" variant="outline" onClick={onCancel}>
                Annuler
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Création...
                  </>
                ) : (
                  'Créer la demande'
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default DemandeForm


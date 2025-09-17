import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Clock, Calendar, Edit, Save, X } from 'lucide-react'

const PlanningAgent = ({ agentId, agentName, canEdit = false, onEdit, refreshTrigger = 0 }) => {
  const [planning, setPlanning] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchPlanning()
  }, [agentId, refreshTrigger])

  const fetchPlanning = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await fetch(`/api/planning/agent/${agentId}`, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        setPlanning(data.planning || {})
      } else {
        const errorData = await response.json()
        setError(errorData.error || 'Erreur lors du chargement du planning')
      }
    } catch (err) {
      console.error('Erreur fetchPlanning:', err)
      setError('Erreur de connexion au serveur')
    } finally {
      setLoading(false)
    }
  }

  const getCreneauClass = (creneau) => {
    if (creneau.en_pause) {
      return 'bg-orange-100 border-orange-300 text-orange-800'
    } else if (creneau.travail) {
      return 'bg-green-100 border-green-300 text-green-800'
    } else {
      return 'bg-gray-100 border-gray-300 text-gray-600'
    }
  }

  const getCreneauText = (creneau) => {
    if (creneau.en_pause) {
      return 'Pause'
    } else if (creneau.travail) {
      return 'Travail'
    } else {
      return 'Libre'
    }
  }

  const calculerTotalHeures = () => {
    let total = 0
    Object.values(planning).forEach(jour => {
      if (jour.plannings && jour.plannings.length > 0) {
        jour.plannings.forEach(planning => {
          total += planning.duree_travail || 0
        })
      }
    })
    return total
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Planning de {agentName}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Chargement du planning...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Planning de {agentName}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-red-600">{error}</p>
            <Button onClick={fetchPlanning} className="mt-4">
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Planning de {agentName}
            </CardTitle>
            <CardDescription>
              Planning hebdomadaire avec créneaux de 30 minutes
            </CardDescription>
          </div>
          {canEdit && (
            <Button onClick={onEdit} variant="outline" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Modifier
            </Button>
          )}
        </div>
        <div className="flex items-center space-x-4 mt-2">
          <Badge variant="outline" className="flex items-center">
            <Clock className="h-3 w-3 mr-1" />
            Total: {calculerTotalHeures()}h/semaine
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {Object.entries(planning).map(([jour, data]) => (
            <div key={jour} className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-lg">{data.jour_nom}</h3>
                {data.plannings && data.plannings.length > 0 && (
                  <div className="text-sm text-gray-600">
                    {data.plannings[0].heure_debut} - {data.plannings[0].heure_fin}
                    {data.plannings[0].pause_debut && data.plannings[0].pause_fin && (
                      <span className="ml-2">
                        (Pause: {data.plannings[0].pause_debut} - {data.plannings[0].pause_fin})
                      </span>
                    )}
                  </div>
                )}
              </div>
              
              {data.creneaux && data.creneaux.length > 0 ? (
                <div className="grid grid-cols-6 gap-1">
                  {data.creneaux.map((creneau, index) => (
                    <div
                      key={index}
                      className={`p-2 text-xs text-center border rounded ${getCreneauClass(creneau)}`}
                      title={`${creneau.heure} - ${getCreneauText(creneau)}`}
                    >
                      <div className="font-medium">{creneau.heure}</div>
                      <div className="text-xs opacity-75">
                        {getCreneauText(creneau)}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  Aucun planning défini pour ce jour
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export default PlanningAgent

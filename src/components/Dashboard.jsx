import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { LogOut, Calendar, Clock, Users, FileText, Settings, User, Building2 } from 'lucide-react'
import AgentDashboard from './AgentDashboard'
import ResponsableDashboard from './ResponsableDashboard'
import ResponsableDashboardTest from './ResponsableDashboardTest'
import AdminDashboard from './AdminDashboard'
import TestAdmin from './TestAdmin'
import SimpleAdmin from './SimpleAdmin'
import AdminTest from './AdminTest'
import AdminDashboardSimple from './AdminDashboardSimple'
import AdminDashboardFixed from './AdminDashboardFixed'
import AdminDashboardNative from './AdminDashboardNative'
import ServicesDebug from './ServicesDebug'
import AgentProfile from './AgentProfile'

const Dashboard = ({ user, onLogout }) => {
  const [loading, setLoading] = useState(false)
  const [currentView, setCurrentView] = useState('dashboard')
  const [selectedAgentId, setSelectedAgentId] = useState(null)

  const handleLogout = async () => {
    setLoading(true)
    try {
      await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include',
      })
      onLogout()
    } catch (err) {
      console.error('Erreur lors de la déconnexion:', err)
      onLogout() // Déconnecter quand même côté client
    } finally {
      setLoading(false)
    }
  }

  const getRoleColor = (role) => {
    switch (role) {
      case 'Admin':
        return 'bg-gradient-to-r from-red-500 to-red-600 text-white shadow-lg'
      case 'Responsable':
        return 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg'
      case 'Agent':
        return 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-lg'
      default:
        return 'bg-gradient-to-r from-gray-500 to-gray-600 text-white shadow-lg'
    }
  }

  const getRoleIcon = (role) => {
    switch (role) {
      case 'Admin':
        return <Settings className="h-4 w-4" />
      case 'Responsable':
        return <Building2 className="h-4 w-4" />
      case 'Agent':
        return <User className="h-4 w-4" />
      default:
        return <User className="h-4 w-4" />
    }
  }

  const handleViewAgent = (agentId) => {
    setSelectedAgentId(agentId)
    setCurrentView('agent-profile')
  }

  const handleBackToDashboard = () => {
    setCurrentView('dashboard')
    setSelectedAgentId(null)
  }

  const handleEditAgent = (agent) => {
    // Retourner au dashboard et déclencher l'édition de l'agent
    setCurrentView('dashboard')
    setSelectedAgentId(null)
    // L'édition sera gérée par le composant AdminDashboardFixed
    console.log('Édition de l\'agent:', agent)
    // On pourrait ajouter un état global pour déclencher l'édition
    // Pour l'instant, l'utilisateur devra cliquer sur l'icône d'édition dans le tableau
  }

  const renderDashboardContent = () => {
    if (currentView === 'agent-profile') {
      return <AgentProfile agentId={selectedAgentId} onBack={handleBackToDashboard} onEditAgent={handleEditAgent} />
    }

    switch (user.role) {
      case 'Agent':
        return <AgentDashboard user={user} />
      case 'Responsable':
        return <ResponsableDashboard user={user} onViewAgent={handleViewAgent} />
      case 'Admin':
        return <AdminDashboardNative user={user} onViewAgent={handleViewAgent} />
      default:
        return <div>Rôle non reconnu</div>
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-50/30">
      {/* Header moderne */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg border-b border-gray-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  Gestion RH
                </h1>
                <p className="text-sm text-gray-600 font-medium">
                  Tableau de bord {user.role}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-900">
                  {user.prenom} {user.nom}
                </p>
                <Badge className={`${getRoleColor(user.role)} flex items-center gap-1 w-fit`}>
                  {getRoleIcon(user.role)}
                  {user.role}
                </Badge>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                disabled={loading}
                className="flex items-center space-x-2 border-red-200 text-red-600 hover:bg-red-50 hover:border-red-300 transition-all duration-200"
              >
                <LogOut className="h-4 w-4" />
                <span>Déconnexion</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {renderDashboardContent()}
      </main>
    </div>
  )
}

export default Dashboard


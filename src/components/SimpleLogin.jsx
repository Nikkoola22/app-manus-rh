import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { User, Calendar, Users } from 'lucide-react'

const SimpleLogin = ({ onLogin }) => {
  const [name, setName] = useState('')
  const [role, setRole] = useState('Agent')
  const [selectedDemoUser, setSelectedDemoUser] = useState(null)

  // Utilisateurs de démonstration disponibles
  const demoUsers = [
    { id: 1, nom: 'Dupont', prenom: 'Jean', email: 'jean.dupont@example.com', role: 'Agent', service_id: 1, service: 'Ressources Humaines' },
    { id: 2, nom: 'Martin', prenom: 'Marie', email: 'marie.martin@example.com', role: 'Responsable', service_id: 1, service: 'Ressources Humaines' },
    { id: 3, nom: 'Bernard', prenom: 'Pierre', email: 'pierre.bernard@example.com', role: 'Agent', service_id: 2, service: 'Informatique' },
    { id: 4, nom: 'Durand', prenom: 'Sophie', email: 'sophie.durand@example.com', role: 'Admin', service_id: 1, service: 'Administration' }
  ] // Force Vercel rebuild - Admin user included

  const handleSubmit = (e) => {
    e.preventDefault()
    if (name.trim()) {
      // Créer un utilisateur simulé
      const user = {
        id: 1,
        nom: name.trim(),
        prenom: name.trim().split(' ')[0],
        email: `${name.toLowerCase().replace(' ', '.')}@example.com`,
        role: role,
        service_id: 1
      }
      onLogin(user)
    }
  }

  const handleDemoUserSelect = (demoUser) => {
    setSelectedDemoUser(demoUser)
    setName(`${demoUser.prenom} ${demoUser.nom}`)
    setRole(demoUser.role)
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

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="w-full max-w-4xl">
        <Card className="shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center space-y-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg mx-auto">
              <Calendar className="h-8 w-8 text-white" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-gray-900 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                Gestion RH - Mode Démo
              </CardTitle>
              <CardDescription className="text-gray-600 mt-2">
                Sélectionnez un utilisateur de démonstration ou créez votre propre profil
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Utilisateurs de démonstration */}
            <div className="space-y-4">
              <div className="flex items-center gap-2 mb-4">
                <Users className="h-5 w-5 text-blue-600" />
                <h3 className="text-lg font-semibold text-gray-800">Utilisateurs de démonstration</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {demoUsers.map((user) => (
                  <Card 
                    key={user.id} 
                    className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                      selectedDemoUser?.id === user.id 
                        ? 'ring-2 ring-blue-500 bg-blue-50' 
                        : 'hover:bg-gray-50'
                    }`}
                    onClick={() => handleDemoUserSelect(user)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold text-gray-900">
                          {user.prenom} {user.nom}
                        </div>
                        <Badge className={getRoleColor(user.role)}>
                          {user.role}
                        </Badge>
                      </div>
                      <div className="text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <User className="h-3 w-3" />
                          {user.email}
                        </div>
                        <div className="mt-1 text-xs text-gray-500">
                          Service: {user.service}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Formulaire personnalisé */}
            <div className="border-t pt-6">
              <div className="flex items-center gap-2 mb-4">
                <User className="h-5 w-5 text-green-600" />
                <h3 className="text-lg font-semibold text-gray-800">Ou créez votre propre profil</h3>
              </div>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                      Votre nom
                    </label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                      <Input
                        id="name"
                        type="text"
                        placeholder="Entrez votre nom"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="pl-10 h-12 text-lg"
                        required
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                      Rôle
                    </label>
                    <select
                      id="role"
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      className="w-full h-12 px-3 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
                    >
                      <option value="Agent">Agent</option>
                      <option value="Responsable">Responsable</option>
                      <option value="Admin">Admin</option>
                    </select>
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full h-12 text-lg font-semibold bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5"
                >
                  Accéder avec ce profil
                </Button>
              </form>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default SimpleLogin

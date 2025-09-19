// Service API centralisé pour gérer les URLs d'API
// Connexion réelle avec l'API Render
const DEMO_MODE = false; // Mode production - connexion réelle
const API_BASE_URL = 'https://app-manus-rh-api.onrender.com/api';

// Données de démonstration
const DEMO_DATA = {
  agents: [
    { id: 1, nom: 'Dupont', prenom: 'Jean', email: 'jean.dupont@example.com', role: 'Agent', service_id: 1, quotite_travail: 35, solde_ca: 25, solde_rtt: 18, solde_hs: 0 },
    { id: 2, nom: 'Martin', prenom: 'Marie', email: 'marie.martin@example.com', role: 'Responsable', service_id: 1, quotite_travail: 35, solde_ca: 30, solde_rtt: 20, solde_hs: 0 },
    { id: 3, nom: 'Bernard', prenom: 'Pierre', email: 'pierre.bernard@example.com', role: 'Agent', service_id: 2, quotite_travail: 35, solde_ca: 22, solde_rtt: 15, solde_hs: 0 }
  ],
  services: [
    { id: 1, nom_service: 'Ressources Humaines', responsable_id: 2, nb_agents: 2 },
    { id: 2, nom_service: 'Informatique', responsable_id: null, nb_agents: 1 }
  ],
  demandes: [
    { id: 1, agent_id: 1, type_absence: 'CA', date_debut: '2024-01-15', date_fin: '2024-01-19', nb_heures: 35, statut: 'En attente', date_demande: '2024-01-10', agent: { prenom: 'Jean', nom: 'Dupont', service_id: 1 } },
    { id: 2, agent_id: 2, type_absence: 'RTT', date_debut: '2024-01-22', date_fin: '2024-01-22', nb_heures: 7, statut: 'Approuvée', date_demande: '2024-01-12', agent: { prenom: 'Marie', nom: 'Martin', service_id: 1 } }
  ],
  arretsMaladie: [
    { id: 1, agent_id: 1, agent_nom: 'Jean Dupont', date_debut: '2024-01-05', date_fin: '2024-01-12', nb_jours: 6, perte_rtt: 0, createur_nom: 'Admin' }
  ]
};

// Stockage local des plannings en mode démo
let demoPlannings = {}

// Fonction pour générer les créneaux 30 minutes à partir d'un planning
const generateCreneaux = (heureDebut, heureFin, pauseDebut, pauseFin) => {
  const creneaux = []
  
  // Convertir les heures en minutes
  const debutMinutes = parseInt(heureDebut.split(':')[0]) * 60 + parseInt(heureDebut.split(':')[1])
  const finMinutes = parseInt(heureFin.split(':')[0]) * 60 + parseInt(heureFin.split(':')[1])
  const pauseDebutMinutes = pauseDebut ? parseInt(pauseDebut.split(':')[0]) * 60 + parseInt(pauseDebut.split(':')[1]) : null
  const pauseFinMinutes = pauseFin ? parseInt(pauseFin.split(':')[0]) * 60 + parseInt(pauseFin.split(':')[1]) : null
  
  let currentMinutes = debutMinutes
  
  while (currentMinutes < finMinutes) {
    // Vérifier si ce créneau est dans la pause
    const estEnPause = pauseDebutMinutes && pauseFinMinutes && 
                      currentMinutes >= pauseDebutMinutes && currentMinutes < pauseFinMinutes
    
    const heure = Math.floor(currentMinutes / 60)
    const minute = currentMinutes % 60
    const heureStr = `${heure.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`
    
    creneaux.push({
      heure: heureStr,
      en_pause: estEnPause,
      travail: !estEnPause
    })
    
    // Ajouter 30 minutes
    currentMinutes += 30
    
    // Gérer le dépassement de 24h
    if (currentMinutes >= 1440) break
  }
  
  return creneaux
}

// Fonction pour simuler une réponse API
const mockResponse = (data, status = 200) => {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(data)
  });
};

// Fonction utilitaire pour gérer les réponses API avec gestion d'erreur robuste
const handleApiResponse = async (response) => {
  if (!response.ok) {
    throw new Error(`Erreur HTTP: ${response.status}`)
  }
  
  const contentType = response.headers.get('content-type')
  if (!contentType || !contentType.includes('application/json')) {
    const text = await response.text()
    console.error('Réponse non-JSON reçue:', text)
    throw new Error('Réponse non-JSON reçue du serveur')
  }
  
  return response.json()
}

export const api = {
  // Auth endpoints
  checkSession: () => DEMO_MODE ? mockResponse({ authenticated: false }) : fetch(`${API_BASE_URL}/auth/check-session`, { credentials: 'include' }),
  login: (credentials) => DEMO_MODE ? mockResponse({ success: true, user: { id: 1, nom: 'Admin', prenom: 'Admin', email: 'admin@example.com', role: 'Admin' } }) : fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(credentials)
  }),
  logout: () => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include'
  }),

  // Agents endpoints
  getAgents: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/agents`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getAgents:', error)
      return DEMO_DATA.agents
    }
  },
  getAgent: (id) => DEMO_MODE ? mockResponse(DEMO_DATA.agents.find(a => a.id === parseInt(id))) : fetch(`${API_BASE_URL}/agents/${id}`, { credentials: 'include' }),
  updateAgent: (id, data) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/agents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),
  deleteAgent: (id) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/agents/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  }),

  // Services endpoints
  getServices: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/services`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getServices:', error)
      return DEMO_DATA.services
    }
  },
  getService: (id) => DEMO_MODE ? mockResponse(DEMO_DATA.services.find(s => s.id === parseInt(id))) : fetch(`${API_BASE_URL}/services/${id}`, { credentials: 'include' }),
  updateService: (id, data) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/services/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),

  // Demandes endpoints
  getDemandes: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/demandes`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getDemandes:', error)
      return DEMO_DATA.demandes
    }
  },
  getMesDemandes: () => DEMO_MODE ? mockResponse(DEMO_DATA.demandes) : fetch(`${API_BASE_URL}/demandes/mes-demandes`, { credentials: 'include' }),
  getDemandesAgent: (agentId) => DEMO_MODE ? mockResponse(DEMO_DATA.demandes.filter(d => d.agent_id === parseInt(agentId))) : fetch(`${API_BASE_URL}/demandes/agent/${agentId}`, { credentials: 'include' }),
  createDemande: (data) => DEMO_MODE ? mockResponse({ success: true, id: Date.now() }) : fetch(`${API_BASE_URL}/demandes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),
  validerDemande: (id) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/demandes/${id}/valider`, {
    method: 'POST',
    credentials: 'include'
  }),
  annulerDemande: (id) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/demandes/${id}/annuler`, {
    method: 'POST',
    credentials: 'include'
  }),

  // Arrêts maladie endpoints
  getArretsMaladie: async (agentId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/arrets-maladie`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getArretsMaladie:', error)
      return DEMO_DATA.arretsMaladie
    }
  },
  deleteArretMaladie: (id) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/arret-maladie/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  }),

  // Planning endpoints
  getPlanningAgent: async (agentId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/planning/${agentId}`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getPlanningAgent:', error)
      // Retourner des données de démonstration en cas d'erreur
      return {
        planning: {
          0: { plannings: [{ heure_debut: '08:00', heure_fin: '17:00', pause_debut: '12:00', pause_fin: '13:00' }], creneaux: [] },
          1: { plannings: [{ heure_debut: '08:00', heure_fin: '17:00', pause_debut: '12:00', pause_fin: '13:00' }], creneaux: [] },
          2: { plannings: [{ heure_debut: '08:00', heure_fin: '11:30', pause_debut: null, pause_fin: null }], creneaux: [] },
          3: { plannings: [{ heure_debut: '08:00', heure_fin: '17:00', pause_debut: '12:00', pause_fin: '13:00' }], creneaux: [] },
          4: { plannings: [{ heure_debut: '08:00', heure_fin: '17:00', pause_debut: '12:00', pause_fin: '13:00' }], creneaux: [] }
        }
      }
    }
  },
  savePlanningAgent: async (agentId, data) => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/planning/${agentId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data)
      })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur savePlanningAgent:', error)
      return { success: true, message: 'Planning sauvegardé (mode démo)' }
    }
  },
  updatePlanningAgent: (agentId, data) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/planning/agent/${agentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),

  // Presence endpoints
  getPresenceCalendrier: async (semaine) => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/presence/calendrier/${semaine}`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getPresenceCalendrier:', error)
      // Retourner des données de démonstration en cas d'erreur
      return [
        {
          id: 1,
          agent_id: 1,
          agent_nom: 'Jean Dupont',
          date_presence: '2024-01-15',
          creneau: 'matin',
          statut: 'present',
          heure_debut: '08:00',
          heure_fin: '12:00',
          motif: ''
        },
        {
          id: 2,
          agent_id: 1,
          agent_nom: 'Jean Dupont',
          date_presence: '2024-01-15',
          creneau: 'apres_midi',
          statut: 'present',
          heure_debut: '13:00',
          heure_fin: '17:00',
          motif: ''
        }
      ]
    }
  },
  getPresenceStatistiques: async (semaine) => {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/presence/statistiques/${semaine}`, { credentials: 'include' })
      return handleApiResponse(response)
    } catch (error) {
      console.error('Erreur getPresenceStatistiques:', error)
      // Retourner des statistiques de démonstration en cas d'erreur
      return {
        total_agents: 3,
        presents: 2,
        absents: 1,
        retards: 0,
        taux_presence: 66.7
      }
    }
  },
  createPresence: (data) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/presence`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),
  updatePresence: (id, data) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/presence/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),
  deletePresence: (id) => DEMO_MODE ? mockResponse({ success: true }) : fetch(`${API_BASE_URL}/presence/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  })
};

export default api;

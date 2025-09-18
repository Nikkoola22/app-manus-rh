// Service API centralisé pour gérer les URLs d'API
// Utilisation directe de l'URL Render
const API_BASE_URL = 'https://app-manus-rh-api.onrender.com/api';

export const api = {
  // Auth endpoints
  checkSession: () => fetch(`${API_BASE_URL}/auth/check-session`, { credentials: 'include' }),
  login: (credentials) => fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(credentials)
  }),
  logout: () => fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include'
  }),

  // Agents endpoints
  getAgents: () => fetch(`${API_BASE_URL}/agents`, { credentials: 'include' }),
  getAgent: (id) => fetch(`${API_BASE_URL}/agents/${id}`, { credentials: 'include' }),
  updateAgent: (id, data) => fetch(`${API_BASE_URL}/agents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),
  deleteAgent: (id) => fetch(`${API_BASE_URL}/agents/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  }),

  // Services endpoints
  getServices: () => fetch(`${API_BASE_URL}/services`, { credentials: 'include' }),
  getService: (id) => fetch(`${API_BASE_URL}/services/${id}`, { credentials: 'include' }),
  updateService: (id, data) => fetch(`${API_BASE_URL}/services/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),

  // Demandes endpoints
  getDemandes: () => fetch(`${API_BASE_URL}/demandes`, { credentials: 'include' }),
  getMesDemandes: () => fetch(`${API_BASE_URL}/demandes/mes-demandes`, { credentials: 'include' }),
  getDemandesAgent: (agentId) => fetch(`${API_BASE_URL}/demandes/agent/${agentId}`, { credentials: 'include' }),
  createDemande: (data) => fetch(`${API_BASE_URL}/demandes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),
  validerDemande: (id) => fetch(`${API_BASE_URL}/demandes/${id}/valider`, {
    method: 'POST',
    credentials: 'include'
  }),
  annulerDemande: (id) => fetch(`${API_BASE_URL}/demandes/${id}/annuler`, {
    method: 'POST',
    credentials: 'include'
  }),

  // Arrêts maladie endpoints
  getArretsMaladie: (agentId) => fetch(`${API_BASE_URL}/arret-maladie${agentId ? `?agent_id=${agentId}` : ''}`, { credentials: 'include' }),
  deleteArretMaladie: (id) => fetch(`${API_BASE_URL}/arret-maladie/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  }),

  // Planning endpoints
  getPlanningAgent: (agentId) => fetch(`${API_BASE_URL}/planning/agent/${agentId}`, { credentials: 'include' }),
  updatePlanningAgent: (agentId, data) => fetch(`${API_BASE_URL}/planning/agent/${agentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }),

  // Presence endpoints
  getPresenceCalendrier: (semaine) => fetch(`${API_BASE_URL}/presence/calendrier/semaine/${semaine}`, { credentials: 'include' }),
  getPresenceStatistiques: (semaine) => fetch(`${API_BASE_URL}/presence/statistiques/semaine/${semaine}`, { credentials: 'include' }),
  deletePresence: (id) => fetch(`${API_BASE_URL}/presence/${id}`, {
    method: 'DELETE',
    credentials: 'include'
  })
};

export default api;

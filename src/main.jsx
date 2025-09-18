import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Force Vercel deployment - Version 0.0.1
console.log('App Manus RH - Version 0.0.2 - Nettoyé et prêt pour production')

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

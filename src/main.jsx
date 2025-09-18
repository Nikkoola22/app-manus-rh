import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Force Vercel deployment - Version 0.0.3 - Cache clear
console.log('App Manus RH - Version 0.0.3 - Cache clear complet')

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

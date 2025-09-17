import { useState } from 'react'
import { Button } from './components/ui/button'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog'

const TestDialog = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div style={{ padding: '20px' }}>
      <h2>Test de Dialog</h2>
      
      <Button onClick={() => setIsOpen(true)}>
        Ouvrir Dialog
      </Button>
      
      <Dialog open={isOpen}>
        <DialogContent onClose={() => setIsOpen(false)}>
          <DialogHeader onClose={() => setIsOpen(false)}>
            <DialogTitle>Test Dialog</DialogTitle>
          </DialogHeader>
          
          <div style={{ padding: '20px' }}>
            <p>Ceci est un test de dialog.</p>
            <p>Vous pouvez fermer ce dialog en :</p>
            <ul>
              <li>Cliquant sur la croix (×)</li>
              <li>Cliquant sur l'arrière-plan</li>
              <li>Appuyant sur Échap</li>
              <li>Cliquant sur le bouton ci-dessous</li>
            </ul>
            
            <Button onClick={() => setIsOpen(false)}>
              Fermer
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default TestDialog





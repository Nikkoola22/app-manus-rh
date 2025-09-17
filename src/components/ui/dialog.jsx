import React from 'react'
import { cn } from '../../lib/utils'

const Dialog = ({ open, onOpenChange, children }) => {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50">
      {children}
    </div>
  )
}

const DialogTrigger = ({ children, onClick }) => {
  return (
    <div onClick={onClick}>
      {children}
    </div>
  )
}

const DialogContent = ({ className, children, onClose, ...props }) => {
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget && onClose) {
      onClose()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Escape' && onClose) {
      onClose()
    }
  }

  React.useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = 'unset'
    }
  }, [])

  return (
    <div
      className={cn(
        'fixed inset-0 z-50 flex items-center justify-center',
        className
      )}
      onClick={handleBackdropClick}
      {...props}
    >
      <div className="fixed inset-0 bg-black/50" />
      <div className="relative z-50 w-full max-w-lg rounded-lg bg-white p-6 shadow-lg">
        {children}
      </div>
    </div>
  )
}

const DialogHeader = ({ className, onClose, ...props }) => (
  <div
    className={cn(
      'flex flex-col space-y-1.5 text-center sm:text-left relative',
      className
    )}
    {...props}
  >
    {onClose && (
      <button
        onClick={onClose}
        className="absolute top-0 right-0 text-gray-400 hover:text-gray-600 text-2xl leading-none w-8 h-8 flex items-center justify-center"
        aria-label="Fermer"
      >
        ×
      </button>
    )}
  </div>
)

const DialogTitle = ({ className, ...props }) => (
  <h2
    className={cn(
      'text-lg font-semibold leading-none tracking-tight',
      className
    )}
    {...props}
  />
)

const DialogDescription = ({ className, ...props }) => (
  <p
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
)

export {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
}


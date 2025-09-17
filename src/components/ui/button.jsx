import React from 'react'
import { cn } from '../../lib/utils'

const Button = React.forwardRef(({ className, variant = 'default', size = 'default', ...props }, ref) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-lg text-sm font-semibold ring-offset-background transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 transform hover:-translate-y-0.5 active:translate-y-0'
  
  const variants = {
    default: 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg hover:shadow-xl hover:from-blue-700 hover:to-blue-800',
    destructive: 'bg-gradient-to-r from-red-500 to-red-600 text-white shadow-lg hover:shadow-xl hover:from-red-600 hover:to-red-700',
    outline: 'border-2 border-gray-200 bg-white/80 backdrop-blur-sm hover:bg-gray-50 hover:border-gray-300 shadow-md hover:shadow-lg',
    secondary: 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-900 shadow-md hover:shadow-lg hover:from-gray-200 hover:to-gray-300',
    ghost: 'hover:bg-gray-100/80 backdrop-blur-sm rounded-lg transition-all duration-200',
    link: 'text-blue-600 underline-offset-4 hover:underline hover:text-blue-700 transition-colors duration-200',
  }
  
  const sizes = {
    default: 'h-11 px-6 py-2',
    sm: 'h-9 rounded-lg px-4 text-xs',
    lg: 'h-13 rounded-lg px-8 text-base',
    icon: 'h-11 w-11 rounded-lg',
  }
  
  return (
    <button
      className={cn(
        baseClasses,
        variants[variant],
        sizes[size],
        className
      )}
      ref={ref}
      {...props}
    />
  )
})

Button.displayName = 'Button'

export { Button }


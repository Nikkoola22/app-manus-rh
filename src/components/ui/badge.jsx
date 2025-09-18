import React from 'react'
import { cn } from '@/lib/lib/utils'

const Badge = React.forwardRef(({ className, variant = 'default', ...props }, ref) => {
  const variants = {
    default: 'inline-flex items-center rounded-full border-0 px-3 py-1 text-xs font-bold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md hover:shadow-lg transform hover:-translate-y-0.5',
    secondary: 'inline-flex items-center rounded-full border-0 px-3 py-1 text-xs font-bold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-gradient-to-r from-gray-500 to-gray-600 text-white shadow-md hover:shadow-lg transform hover:-translate-y-0.5',
    destructive: 'inline-flex items-center rounded-full border-0 px-3 py-1 text-xs font-bold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-gradient-to-r from-red-500 to-red-600 text-white shadow-md hover:shadow-lg transform hover:-translate-y-0.5',
    outline: 'inline-flex items-center rounded-full border-2 border-gray-200 px-3 py-1 text-xs font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-white/80 backdrop-blur-sm text-gray-700 shadow-sm hover:shadow-md',
  }

  return (
    <div
      ref={ref}
      className={cn(variants[variant], className)}
      {...props}
    />
  )
})

Badge.displayName = 'Badge'

export { Badge }


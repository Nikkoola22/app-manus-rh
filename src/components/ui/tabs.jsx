import React, { createContext, useContext, useState } from 'react'
import { cn } from '../../lib/utils'

const TabsContext = createContext()

const Tabs = React.forwardRef(({ className, defaultValue, value, onValueChange, children, ...props }, ref) => {
  const [internalValue, setInternalValue] = useState(defaultValue || '')
  const currentValue = value !== undefined ? value : internalValue

  const handleValueChange = (newValue) => {
    if (value === undefined) {
      setInternalValue(newValue)
    }
    if (onValueChange) {
      onValueChange(newValue)
    }
  }

  return (
    <TabsContext.Provider value={{ value: currentValue, onValueChange: handleValueChange }}>
      <div ref={ref} className={cn('w-full', className)} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  )
})
Tabs.displayName = 'Tabs'

const TabsList = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'inline-flex h-12 items-center justify-center rounded-2xl bg-gradient-to-r from-gray-100 to-gray-200/50 p-1.5 text-gray-600 shadow-lg',
      className
    )}
    {...props}
  />
))
TabsList.displayName = 'TabsList'

const TabsTrigger = React.forwardRef(({ className, value, ...props }, ref) => {
  const context = useContext(TabsContext)
  const isActive = context.value === value

  const handleClick = () => {
    if (context.onValueChange && value) {
      context.onValueChange(value)
    }
  }

  return (
    <button
      ref={ref}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-xl px-6 py-2.5 text-sm font-bold ring-offset-background transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-purple-600 data-[state=active]:text-white data-[state=active]:shadow-lg transform data-[state=active]:-translate-y-0.5',
        isActive && 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg transform -translate-y-0.5',
        className
      )}
      onClick={handleClick}
      data-state={isActive ? 'active' : 'inactive'}
      {...props}
    />
  )
})
TabsTrigger.displayName = 'TabsTrigger'

const TabsContent = React.forwardRef(({ className, value, ...props }, ref) => {
  const context = useContext(TabsContext)
  const isActive = context.value === value

  if (!isActive) {
    return null
  }

  return (
    <div
      ref={ref}
      className={cn(
        'mt-6 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        className
      )}
      {...props}
    />
  )
})
TabsContent.displayName = 'TabsContent'

export { Tabs, TabsList, TabsTrigger, TabsContent }


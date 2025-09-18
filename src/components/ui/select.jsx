import React, { useState, useRef, useEffect } from 'react'
import { cn } from '@/lib/utils.jsx'
import { ChevronDown } from 'lucide-react'

const Select = ({ value, onValueChange, children, ...props }) => {
  const [isOpen, setIsOpen] = useState(false)
  const selectRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (selectRef.current && !selectRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelect = (value) => {
    onValueChange(value)
    setIsOpen(false)
  }

  return (
    <div ref={selectRef} className="relative" {...props}>
      {React.Children.map(children, child => {
        if (child.type.displayName === 'SelectTrigger') {
          return React.cloneElement(child, { 
            onClick: () => setIsOpen(!isOpen),
            isOpen 
          })
        }
        if (child.type.displayName === 'SelectContent') {
          return isOpen ? React.cloneElement(child, { 
            onSelect: handleSelect,
            value 
          }) : null
        }
        return child
      })}
    </div>
  )
}

const SelectTrigger = React.forwardRef(({ className, children, onClick, isOpen, ...props }, ref) => (
  <button
    ref={ref}
    type="button"
    onClick={onClick}
    className={cn(
      'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
      className
    )}
    {...props}
  >
    {children}
    <ChevronDown className={cn("h-4 w-4 opacity-50 transition-transform", isOpen && "rotate-180")} />
  </button>
))
SelectTrigger.displayName = 'SelectTrigger'

const SelectValue = React.forwardRef(({ className, placeholder, ...props }, ref) => (
  <span
    ref={ref}
    className={cn(className)}
    {...props}
  >
    {props.children || placeholder}
  </span>
))
SelectValue.displayName = 'SelectValue'

const SelectContent = React.forwardRef(({ className, children, onSelect, value, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'absolute z-50 w-full max-h-96 min-w-[8rem] overflow-hidden rounded-md border border-gray-300 bg-white text-gray-900 shadow-lg top-full mt-1',
      className
    )}
    {...props}
  >
    <div className="p-1">
      {React.Children.map(children, child => {
        if (child.type.displayName === 'SelectItem') {
          return React.cloneElement(child, { 
            onClick: () => onSelect(child.props.value),
            isSelected: child.props.value === value
          })
        }
        return child
      })}
    </div>
  </div>
))
SelectContent.displayName = 'SelectContent'

const SelectItem = React.forwardRef(({ className, children, onClick, isSelected, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'relative flex w-full cursor-pointer select-none items-center rounded-sm py-2 px-3 text-sm outline-none hover:bg-blue-50 hover:text-blue-900 data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      isSelected && 'bg-blue-100 text-blue-900',
      className
    )}
    onClick={onClick}
    {...props}
  >
    {children}
  </div>
))
SelectItem.displayName = 'SelectItem'

export {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
}


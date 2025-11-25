import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

type Option = string | { value: string; label: string }

interface SelectProps {
  label?: string
  value?: string
  options: Option[]
  placeholder?: string
  disabled?: boolean
  onChange?: (value: string) => void
  style?: React.CSSProperties
}

export function Select({
  label,
  value,
  options,
  placeholder = 'Select an option...',
  disabled = false,
  onChange,
  style,
}: SelectProps) {
  const [isOpen, setIsOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const normalizedOptions = options.map(opt =>
    typeof opt === 'string' ? { value: opt, label: opt } : opt
  )

  const selectedOption = normalizedOptions.find(opt => opt.value === value)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4 relative"
      style={style}
    >
      {label && (
        <label className="block text-sm font-medium text-text mb-1.5">
          {label}
        </label>
      )}
      <button
        type="button"
        disabled={disabled}
        onClick={() => setIsOpen(!isOpen)}
        className={`
          w-full px-4 py-2.5 rounded-lg text-sm text-left
          bg-surface border-2 flex items-center justify-between
          transition-all duration-200
          disabled:opacity-50 disabled:cursor-not-allowed
          focus:outline-none
          ${isOpen
            ? 'border-primary shadow-sm'
            : 'border-border hover:border-border-hover'
          }
        `}
      >
        <span className={selectedOption ? 'text-text' : 'text-text-tertiary'}>
          {selectedOption?.label || placeholder}
        </span>
        <motion.svg
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="w-5 h-5 text-text-tertiary"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </motion.svg>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="absolute z-50 w-full mt-1 bg-surface border border-border rounded-lg shadow-lg overflow-hidden"
          >
            <div className="max-h-60 overflow-y-auto py-1">
              {normalizedOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => {
                    onChange?.(option.value)
                    setIsOpen(false)
                  }}
                  className={`
                    w-full px-4 py-2.5 text-sm text-left
                    transition-colors duration-150
                    ${option.value === value
                      ? 'bg-primary/10 text-primary font-medium'
                      : 'text-text hover:bg-surface-hover'
                    }
                  `}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

interface MultiSelectProps {
  label?: string
  value: string[]
  options: Option[]
  placeholder?: string
  disabled?: boolean
  onChange?: (value: string[]) => void
  style?: React.CSSProperties
}

export function MultiSelect({
  label,
  value,
  options,
  placeholder = 'Select options...',
  disabled = false,
  onChange,
  style,
}: MultiSelectProps) {
  const [isOpen, setIsOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const normalizedOptions = options.map(opt =>
    typeof opt === 'string' ? { value: opt, label: opt } : opt
  )

  const selectedOptions = normalizedOptions.filter(opt => value.includes(opt.value))

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const toggleOption = (optValue: string) => {
    const newValue = value.includes(optValue)
      ? value.filter(v => v !== optValue)
      : [...value, optValue]
    onChange?.(newValue)
  }

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4 relative"
      style={style}
    >
      {label && (
        <label className="block text-sm font-medium text-text mb-1.5">
          {label}
        </label>
      )}
      <button
        type="button"
        disabled={disabled}
        onClick={() => setIsOpen(!isOpen)}
        className={`
          w-full px-4 py-2.5 rounded-lg text-sm text-left
          bg-surface border-2 flex items-center justify-between
          transition-all duration-200 min-h-[42px]
          disabled:opacity-50 disabled:cursor-not-allowed
          focus:outline-none
          ${isOpen
            ? 'border-primary shadow-sm'
            : 'border-border hover:border-border-hover'
          }
        `}
      >
        <div className="flex flex-wrap gap-1 flex-1">
          {selectedOptions.length > 0 ? (
            selectedOptions.map(opt => (
              <span
                key={opt.value}
                className="inline-flex items-center px-2 py-0.5 rounded bg-primary/10 text-primary text-xs font-medium"
              >
                {opt.label}
              </span>
            ))
          ) : (
            <span className="text-text-tertiary">{placeholder}</span>
          )}
        </div>
        <motion.svg
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="w-5 h-5 text-text-tertiary ml-2 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </motion.svg>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="absolute z-50 w-full mt-1 bg-surface border border-border rounded-lg shadow-lg overflow-hidden"
          >
            <div className="max-h-60 overflow-y-auto py-1">
              {normalizedOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => toggleOption(option.value)}
                  className={`
                    w-full px-4 py-2.5 text-sm text-left flex items-center gap-3
                    transition-colors duration-150
                    ${value.includes(option.value)
                      ? 'bg-primary/10 text-primary'
                      : 'text-text hover:bg-surface-hover'
                    }
                  `}
                >
                  <div className={`
                    w-4 h-4 rounded border-2 flex items-center justify-center
                    transition-colors duration-150
                    ${value.includes(option.value)
                      ? 'bg-primary border-primary'
                      : 'border-border'
                    }
                  `}>
                    {value.includes(option.value) && (
                      <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                  {option.label}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

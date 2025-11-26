import React, { useState } from 'react'
import { motion } from 'framer-motion'

interface InputProps {
  id?: string
  label?: string
  value: string
  placeholder?: string
  type?: string
  disabled?: boolean
  onChange?: (value: string) => void
  style?: React.CSSProperties
}

export function Input({
  id,
  label,
  value,
  placeholder,
  type = 'text',
  disabled = false,
  onChange,
  style,
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4"
      style={style}
    >
      {label && (
        <label className="block text-sm font-medium text-text mb-1.5">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          id={id}
          type={type}
          value={value}
          placeholder={placeholder}
          disabled={disabled}
          onChange={(e) => onChange?.(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className={`
            w-full px-4 py-2.5 rounded-lg text-sm
            bg-surface border-2 text-text
            placeholder:text-text-tertiary
            transition-all duration-200
            disabled:opacity-50 disabled:cursor-not-allowed
            focus:outline-none
            ${isFocused
              ? 'border-primary shadow-sm'
              : 'border-border hover:border-border-hover'
            }
          `}
        />
        {isFocused && (
          <motion.div
            layoutId="input-focus"
            className="absolute inset-0 rounded-lg ring-2 ring-primary/20 pointer-events-none"
            initial={false}
            transition={{ duration: 0.15 }}
          />
        )}
      </div>
    </motion.div>
  )
}

interface TextAreaProps {
  id?: string
  label?: string
  value: string
  placeholder?: string
  rows?: number
  disabled?: boolean
  onChange?: (value: string) => void
  style?: React.CSSProperties
}

export function TextArea({
  id,
  label,
  value,
  placeholder,
  rows = 4,
  disabled = false,
  onChange,
  style,
}: TextAreaProps) {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4"
      style={style}
    >
      {label && (
        <label className="block text-sm font-medium text-text mb-1.5">
          {label}
        </label>
      )}
      <textarea
        id={id}
        value={value}
        placeholder={placeholder}
        rows={rows}
        disabled={disabled}
        onChange={(e) => onChange?.(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className={`
          w-full px-4 py-2.5 rounded-lg text-sm
          bg-surface border-2 text-text
          placeholder:text-text-tertiary
          transition-all duration-200 resize-y
          disabled:opacity-50 disabled:cursor-not-allowed
          focus:outline-none
          ${isFocused
            ? 'border-primary shadow-sm'
            : 'border-border hover:border-border-hover'
          }
        `}
      />
    </motion.div>
  )
}

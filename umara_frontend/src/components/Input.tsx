import React, { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'

interface InputProps {
  id?: string
  label?: string
  value: string
  placeholder?: string
  type?: string
  disabled?: boolean
  maxChars?: number
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
  maxChars,
  onChange,
  style,
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false)
  // Use uncontrolled input pattern - only sync with server on blur
  const inputRef = useRef<HTMLInputElement>(null)

  // Initialize input value from prop on mount
  useEffect(() => {
    if (inputRef.current && !isFocused) {
      inputRef.current.value = value
    }
  }, [value, isFocused])

  const handleFocus = () => {
    setIsFocused(true)
  }

  const handleBlur = () => {
    setIsFocused(false)
    // Send final value to server on blur
    if (inputRef.current) {
      const newValue = inputRef.current.value
      if (newValue !== value) {
        onChange?.(newValue)
      }
    }
  }

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
          {maxChars && (
            <span className="text-text-tertiary ml-2 font-normal">
              ({value.length}/{maxChars})
            </span>
          )}
        </label>
      )}
      <div className="relative">
        <input
          ref={inputRef}
          id={id}
          type={type}
          defaultValue={value}
          placeholder={placeholder}
          disabled={disabled}
          maxLength={maxChars}
          onFocus={handleFocus}
          onBlur={handleBlur}
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
  height?: number
  disabled?: boolean
  maxChars?: number
  onChange?: (value: string) => void
  style?: React.CSSProperties
}

export function TextArea({
  id,
  label,
  value,
  placeholder,
  rows = 4,
  height,
  disabled = false,
  maxChars,
  onChange,
  style,
}: TextAreaProps) {
  const [isFocused, setIsFocused] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Initialize textarea value from prop on mount
  useEffect(() => {
    if (textareaRef.current && !isFocused) {
      textareaRef.current.value = value
    }
  }, [value, isFocused])

  const handleFocus = () => {
    setIsFocused(true)
  }

  const handleBlur = () => {
    setIsFocused(false)
    if (textareaRef.current) {
      const newValue = textareaRef.current.value
      if (newValue !== value) {
        onChange?.(newValue)
      }
    }
  }

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
          {maxChars && (
            <span className="text-text-tertiary ml-2 font-normal">
              ({value.length}/{maxChars})
            </span>
          )}
        </label>
      )}
      <textarea
        ref={textareaRef}
        id={id}
        defaultValue={value}
        placeholder={placeholder}
        rows={height ? undefined : rows}
        disabled={disabled}
        maxLength={maxChars}
        onFocus={handleFocus}
        onBlur={handleBlur}
        style={height ? { height: `${height}px` } : undefined}
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

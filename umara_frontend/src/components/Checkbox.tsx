import React from 'react'
import { motion } from 'framer-motion'

interface CheckboxProps {
  label: string
  checked: boolean
  disabled?: boolean
  onChange?: (checked: boolean) => void
  style?: React.CSSProperties
}

export function Checkbox({
  label,
  checked,
  disabled = false,
  onChange,
  style,
}: CheckboxProps) {
  return (
    <motion.label
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`
        flex items-center gap-3 cursor-pointer mb-3 select-none
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
      style={style}
    >
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          disabled={disabled}
          onChange={(e) => onChange?.(e.target.checked)}
          className="sr-only"
        />
        <motion.div
          className={`
            w-5 h-5 rounded border-2 flex items-center justify-center
            transition-colors duration-200
            ${checked
              ? 'bg-primary border-primary'
              : 'bg-surface border-border hover:border-border-hover'
            }
          `}
          whileTap={{ scale: 0.9 }}
        >
          <motion.svg
            initial={false}
            animate={{
              scale: checked ? 1 : 0,
              opacity: checked ? 1 : 0,
            }}
            transition={{ duration: 0.15 }}
            className="w-3.5 h-3.5 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={3}
              d="M5 13l4 4L19 7"
            />
          </motion.svg>
        </motion.div>
      </div>
      <span className="text-sm text-text">{label}</span>
    </motion.label>
  )
}

interface ToggleProps {
  label: string
  checked: boolean
  disabled?: boolean
  onChange?: (checked: boolean) => void
  style?: React.CSSProperties
}

export function Toggle({
  label,
  checked,
  disabled = false,
  onChange,
  style,
}: ToggleProps) {
  return (
    <motion.label
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`
        flex items-center gap-3 cursor-pointer mb-3 select-none
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
      style={style}
    >
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        disabled={disabled}
        onClick={() => onChange?.(!checked)}
        className={`
          relative w-11 h-6 rounded-full
          transition-colors duration-200
          focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2
          ${checked ? 'bg-primary' : 'bg-border'}
        `}
      >
        <motion.div
          className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-md"
          animate={{ x: checked ? 20 : 0 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        />
      </button>
      <span className="text-sm text-text">{label}</span>
    </motion.label>
  )
}

interface RadioProps {
  label: string
  value?: string
  options: string[]
  horizontal?: boolean
  disabled?: boolean
  onChange?: (value: string) => void
  style?: React.CSSProperties
}

export function Radio({
  label,
  value,
  options,
  horizontal = false,
  disabled = false,
  onChange,
  style,
}: RadioProps) {
  return (
    <motion.fieldset
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      {label && (
        <legend className="text-sm font-medium text-text mb-2">
          {label}
        </legend>
      )}
      <div className={`
        ${horizontal ? 'flex flex-wrap gap-4' : 'space-y-2'}
      `}>
        {options.map((option) => (
          <label
            key={option}
            className={`
              flex items-center gap-3 cursor-pointer select-none
              ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            <div className="relative">
              <input
                type="radio"
                name={label}
                value={option}
                checked={value === option}
                disabled={disabled}
                onChange={() => onChange?.(option)}
                className="sr-only"
              />
              <motion.div
                className={`
                  w-5 h-5 rounded-full border-2
                  transition-colors duration-200
                  ${value === option
                    ? 'border-primary'
                    : 'border-border hover:border-border-hover'
                  }
                `}
                whileTap={{ scale: 0.9 }}
              >
                <motion.div
                  className="absolute inset-1.5 rounded-full bg-primary"
                  initial={false}
                  animate={{
                    scale: value === option ? 1 : 0,
                    opacity: value === option ? 1 : 0,
                  }}
                  transition={{ duration: 0.15 }}
                />
              </motion.div>
            </div>
            <span className="text-sm text-text">{option}</span>
          </label>
        ))}
      </div>
    </motion.fieldset>
  )
}

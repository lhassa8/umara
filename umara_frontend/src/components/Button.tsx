import React from 'react'
import { motion } from 'framer-motion'

interface ButtonProps {
  label: string
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  disabled?: boolean
  fullWidth?: boolean
  onClick?: () => void
  style?: React.CSSProperties
}

export function Button({
  label,
  variant = 'primary',
  disabled = false,
  fullWidth = false,
  onClick,
  style,
}: ButtonProps) {
  const baseClasses = `
    inline-flex items-center justify-center
    px-5 py-2.5 rounded-lg font-medium text-sm
    transition-all duration-200 ease-out
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `

  const variantClasses: Record<string, string> = {
    primary: `
      bg-primary text-white
      hover:bg-primary-hover active:bg-primary-active
      focus:ring-primary/50
      shadow-sm hover:shadow-md
    `,
    secondary: `
      bg-secondary-light text-secondary
      hover:bg-secondary-light/80 active:bg-secondary-light
      focus:ring-secondary/30
    `,
    outline: `
      bg-transparent text-primary border-2 border-primary
      hover:bg-primary/5 active:bg-primary/10
      focus:ring-primary/50
    `,
    ghost: `
      bg-transparent text-text
      hover:bg-secondary-light active:bg-secondary-light/80
      focus:ring-secondary/30
    `,
    danger: `
      bg-error text-white
      hover:bg-error-dark active:bg-error-dark
      focus:ring-error/50
      shadow-sm hover:shadow-md
    `,
  }

  return (
    <motion.button
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      className={`
        ${baseClasses}
        ${variantClasses[variant]}
        ${fullWidth ? 'w-full' : ''}
      `}
      disabled={disabled}
      onClick={onClick}
      style={style}
    >
      {label}
    </motion.button>
  )
}
